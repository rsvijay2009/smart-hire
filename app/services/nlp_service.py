import spacy
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load skills from JSON
with open(Path(__file__).parent.parent / "data" / "skills.json", "r") as f:
    SKILL_KEYWORDS = json.load(f)["skills"]

# Load qualifications from JSON
with open(Path(__file__).parent.parent / "data" / "qualifications.json", "r") as f:
    QUALIFICATION_KEYWORDS = json.load(f)["qualifications"]

def extract_skills_experience(text):
    """
    Extract skills and experience from text using NLP.

    Args:
        text (str): Input text to process.

    Returns:
        tuple: List of skills and years of experience.
    """
    try:
        doc = nlp(text)
        skills = set()
        experience = 0

        # Extract skills
        for token in doc:
            if token.text.lower() in SKILL_KEYWORDS:
                skills.add(token.text.lower())

        # Extract experience
        pattern = r"(\d+)\s*(?:year|years)\s*(?:of\s*)?(?:experience)?"
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            experience = max([int(y) for y in matches], default=0)

        logger.info(f"Extracted {len(skills)} skills and {experience} years experience.")
        return list(skills), experience
    except Exception as e:
        logger.error(f"Error extracting skills/experience: {e}")
        return [], 0

def calculate_match_score(job_text, resume_text, job_skills, job_experience):
    """
    Calculate a weighted match score for a candidate.

    Args:
        job_text (str): Job description text.
        resume_text (str): Resume text.
        job_skills (list): Required skills from job.
        job_experience (int): Required years of experience.

    Returns:
        tuple: Match score, skills, experience, qualifications.
    """
    try:
        # Extract resume details
        resume_skills, resume_experience = extract_skills_experience(resume_text)
        qualifications = extract_qualifications(resume_text)

        # Text similarity
        job_doc = nlp(job_text)
        resume_doc = nlp(resume_text)
        text_similarity = 0.0
        if job_doc.vector_norm and resume_doc.vector_norm:
            text_similarity = cosine_similarity([job_doc.vector], [resume_doc.vector])[0][0]

        # Skill match
        skill_overlap = len(set(job_skills) & set(resume_skills)) / max(len(job_skills), 1)
        if not resume_skills:
            skill_overlap *= 0.5  # Penalize missing skills

        # Experience match
        experience_diff = abs(job_experience - resume_experience)
        experience_score = max(0, 1 - (experience_diff / max(job_experience, 1)))

        # Qualification match (simplified)
        qualification_score = 1.0 if qualifications else 0.5

        # Weighted score
        final_score = (
            0.4 * text_similarity
            + 0.3 * skill_overlap
            + 0.2 * experience_score
            + 0.1 * qualification_score
        )

        logger.info(f"Calculated match score: {final_score}")
        return final_score, resume_skills, resume_experience, qualifications
    except Exception as e:
        logger.error(f"Error calculating match score: {e}")
        return 0.0, [], 0, []

def extract_qualifications(text):
    """
    Extract qualifications from text using both NER and token-based search.

    Args:
        text (str): Input text.

    Returns:
        list: List of qualifications.
    """
    qualifications = []
    doc = nlp(text)
    logger.info(f"Entities found: {[(ent.text, ent.label_) for ent in doc.ents]}")

    # NER-based extraction
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            if any(keyword in ent.text.lower() for keyword in QUALIFICATION_KEYWORDS):
                qualifications.append(ent.text)
                logger.info(f"NER qualification extracted: {ent.text}")

    # Token-based extraction for degrees not tagged as entities
    degree_pattern = r"(?:B\.Sc\.?|M\.Sc\.?|Ph\.D\.?|MBA|Bachelor|Master|Doctorate)\s*(?:in\s*[\w\s]+)?"
    matches = re.findall(degree_pattern, text, re.IGNORECASE)
    for match in matches:
        if match not in qualifications:
            qualifications.append(match)
            logger.info(f"Token-based qualification extracted: {match}")

    if not qualifications:
        logger.info("No qualifications extracted.")
    return qualifications