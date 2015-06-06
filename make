APP=PseudoBusy
MAIN=__main__.py
[[ -d $APP ]] || mkdir $APP
cp *.py $APP
cd $APP
touch $MAIN || exit
> $MAIN
printf '#!/usr/bin/env python\nimport pseudoBusy\nif __name__ == "__main__":\n    main=pseudoBusy.PseudoBusy()\n    main.run()' >> $MAIN
zip -r ../$APP *
cd ..
rm -rf $APP
mv $APP.zip $APP
