#!/bin/bash
git add .
git commit -m 'update'
git push origin source
bundle exec rake generate
bundle exec rake deploy
