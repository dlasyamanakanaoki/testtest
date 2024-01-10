#/bin/bash

VERSION_FILE_PATH=version.txt
VERSION_TXT=`cat ${VERSION_FILE_PATH}`

if [[ ${VERSION_TXT} =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
    NEW_VERSION="v${BASH_REMATCH[1]}.${BASH_REMATCH[2]}.$((BASH_REMATCH[3] + 1))"
    printf ${NEW_VERSION} > ${VERSION_FILE_PATH} 
    echo "update version number ${VERSION_TXT} > ${NEW_VERSION}"
else
    echo ${VERSION_TXT}
fi
