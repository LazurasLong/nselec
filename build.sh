#!/bin/bash
# use -d for a dry run
dr=
[ "$1" == "-d" ] && dr=echo
ver=$(python -c 'from nselec import __version__ as v;print(v)')
read -p "Building v$ver - continue? [y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  $dr git tag -s -a "v$ver" -m "Version $ver"
  $dr git push origin "v$ver"
  $dr python setup.py sdist bdist_wheel
  $dr twine upload dist/nselec-${ver}*
  echo "Done!"
else
  echo "Ok, have a nice day"
fi
exit 0

