#!/bin/bash
mkdir -p /opt/render/project/src/app/uploads
chmod -R 755 /opt/render/project/src/app/uploads
chown -R nobody:nobody /opt/render/project/src/app/uploads
exec gunicorn run:app