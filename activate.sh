if [ -s ./.venv ] ; then 
	. ./.venv/bin/activate ;
else
	echo 'No venv defined, creating...' ;
	venvprompt=${PWD##*/}
	python -m venv --prompt $venvprompt .venv ;
	. ./.venv/bin/activate ;
fi;

