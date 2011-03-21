#! /bin/bash

jslint test/good.js > test/good.actual
if diff test/good.golden test/good.actual
then
    echo OK
else
    echo FAIL
    exit 1
fi

jslint test/bad.js > test/bad.actual
if diff test/bad.golden test/bad.actual
then
    echo OK
else
    echo FAIL
    exit 1
fi

