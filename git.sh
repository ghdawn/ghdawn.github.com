#!/bin/bash
git add .
git commit -m 'update'
git push origin source
rake-ruby-1.9.2-p290 generate
rake-ruby-1.9.2-p290 deploy
