#!/bin/sh

usage() {
	echo "ERROR"
	exit 1
}

while getopts "r:" arg
do
	case ${arg} in
		r)
			request="${OPTARG}"
		;;
		*) usage
		;;
	esac   # is ridiculous ;-)
done
shift $((OPTIND-1))

url="$1"
shift

if [ -z "${request}" ]
then
	curl localhost:4000/${url}
else
	if [ -f 'auth' ]
	then
		auth="Authorization: Bearer `cat auth`"
		curl -d @${request} -H "Content-Type: application/json" -H "${auth}" localhost:4000/${url}
	else
		curl -d @${request} -H "Content-Type: application/json" localhost:4000/${url}
	fi
fi

