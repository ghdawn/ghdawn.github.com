git add .
git commit -m 'update'
git push origin pelican_source
make html
./output/deploy.sh