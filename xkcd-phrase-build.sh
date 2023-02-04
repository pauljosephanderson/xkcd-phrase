!/usr/bin/env bash

###############################################################
#  Build and locally deploy xkcd-pass                         #
###############################################################

# establish varaibles
PROJECT="xkcd-phrase"

# ensure latest version of pip, build and twine (twine is to allow upload to pip repository)
python3 -m pip install --upgrade pip build twine pytest

# clean-up
python3 -m pip uninstall ${PROJECT} -y
#python3 cache remove ${PROJECT}

# Building Package
if [ $(find -name pyproject.toml) = "./pyproject.toml" ]
then
	python3 -m build
	PACKAGE=$(find -type f -name ${PROJECT}"*" | grep dist)

#	local deploy of Package
	echo ************************************************************************************************************
	echo *                                                                                                          *
	echo * This is doing a local install                                                                            *
	echo * To do an install into PIP, refer to https://packaging.python.org/en/latest/tutorials/packaging-projects/ *
	echo *                                                                                                          *
	echo ************************************************************************************************************
	python3 -m pip install ${PACKAGE} --force-reinstall

	echo ************************************************************************************************************
	echo *                                                                                                          *
	echo * validate deployed pacakge                                                                                *
	echo *                                                                                                          *
	echo ************************************************************************************************************
	pytest -v > tests/test.out
	pytest -v

	echo ************************************************************************************************************
	echo *                                                                                                          *
	echo * run deployed pacakge                                                                                     *
	echo *                                                                                                          *
	echo ************************************************************************************************************
	${PROJECT} -a test -c 12

else
	echo Script must be run from directory with pyproject.toml in it.  Exiting and good-bye.
fi
exit 0
