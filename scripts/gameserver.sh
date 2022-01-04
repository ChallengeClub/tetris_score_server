#!/bin/bash

# prepare
#   - install docker
#   - prepare to push to github
#       if necessary, write ~/.netrc
#          see https://qiita.com/azusanakano/items/8dc1d7e384b00239d4d9
#   - export API_KEY="xxx"
#       if necessary, see https://qiita.com/seigot/items/77cf8ce36023c273232d
#   - update current idx
#       $ echo 0 > current_idx.txt
#   - do main process
#       $ bash gameserver.sh -m release

## get args level setting
EXEC_MODE="DEBUG"  # DEBUG or RELEASE
while getopts m: OPT
do
  case $OPT in
    "m" ) EXEC_MODE="$OPTARG" ;;
  esac
done
echo "EXEC_MODE: ${EXEC_MODE}"


function update_result(){
    # update to github
    # https://github.com/seigot/tetris_score_server

    DATETIME="$1" #`date +%Y%m%d_%H%M_%S`
    REPOSITORY_URL="$2"
    SCORE="$3"
    LEVEL="$4"
    RESULT="$5"
    STR="${DATETIME}, ${REPOSITORY_URL}, ${SCORE}, ${LEVEL}, ${RESULT}"    

    ## update result file
    RESULT_CSV="result.csv"
    RESULT_LEVEL_LOG="result_level_${LEVEL}.log"
    RESULT_RANKING_LOG="result_ranking_level_${LEVEL}.log"

    echo $STR >> ${RESULT_CSV}

    if [ "${RESULT}" == "SUCCESS" ]; then
	if [ ! -e ${RESULT_LEVEL_LOG} ]; then
	    echo "DATETIME, REPOSITORY_URL, SCORE, LEVEL, RESULT" >> ${RESULT_LEVEL_LOG}
	    echo "---" >> ${RESULT_LEVEL_LOG}
	fi
	echo $STR >> ${RESULT_LEVEL_LOG}
	cat <(head -2 ${RESULT_LEVEL_LOG}) <(tail -n +3 ${RESULT_LEVEL_LOG} | sort -nr -t, -k3 | column -t -s,) > ${RESULT_RANKING_LOG}
    fi
	
    echo "--"
    cat ${RESULT_CSV}
    echo "--"
    cat ${RESULT_LEVEL_LOG}
    echo "--"
    cat ${RESULT_RANKING_LOG}

    # skip if not release mode
    if [ "${EXEC_MODE}" != "RELEASE" ];then
	echo "skip update to git"
	echo "  EXEC_MODE: ${EXEC_MODE}"
	return 0
    fi

    ## update to score server
    #git clone https://github.com/seigot/tetris_score_server
    #pushd tetris_score_server/logs
    git pull
    git add ${RESULT_CSV}
    git add ${RESULT_LEVEL_LOG}
    git add ${RESULT_RANKING_LOG}
    git commit -m "update result"
    git push
    #popd
}

function error_result(){

    #DATETIME="$1" #`date +%Y%m%d_%H%M_%S`
    #REPOSITORY_URL="$2"
    #SCORE="$3"
    #LEVEL="$4"
    #RESULT="$5"
    #STR="${DATETIME}, ${REPOSITORY_URL}, ${SCORE}, ${LEVEL}, ${RESULT}"
    #update_result "${STR}"
    update_result "$1" "$2" "$3" "$4" "$5"
}

function success_result(){

    #DATETIME="$1" #`date +%Y%m%d_%H%M_%S`
    #REPOSITORY_URL="$2"
    #SCORE="$3"
    #LEVEL="$4"
    #STR="${DATETIME}, ${REPOSITORY_URL}, ${SCORE}, ${LEVEL}, SUCCESS"
    #update_result "${STR}"
    update_result "$1" "$2" "$3" "$4" "SUCCESS"
}

function do_tetris(){

    DATETIME="$1"
    REPOSITORY_URL="$2"
    LEVEL="$3"
    GAME_TIME="180"
    if [ "${EXEC_MODE}" != "RELEASE" ]; then
	GAME_TIME="3" # debug value
    fi 
    
    PRE_COMMAND="cd ~ && rm -rf tetris && git clone ${REPOSITORY_URL} && cd ~/tetris && pip3 install -r requirements.txt"
    DO_COMMAND="cd ~/tetris && export DISPLAY=:1 && python3 start.py -l ${LEVEL} -t ${GAME_TIME} && jq . result.json"
    POST_COMMAND="cd ~/tetris && jq .judge_info.score result.json"

    TMP_LOG="tmp.log"
    CONTAINER_NAME="tetris_docker"

    # run docker with detached state
    RET=`docker ps -a | grep ${CONTAINER_NAME} | wc -l`
    if [ $RET -ne 0 ]; then
	docker stop ${CONTAINER_NAME}
	docker rm ${CONTAINER_NAME}
    fi
    docker run -d --name ${CONTAINER_NAME} -p 6080:80 --shm-size=512m seigott/tetris_docker

    # exec command
    docker exec ${CONTAINER_NAME} bash -c "${PRE_COMMAND}"
    if [ $? -ne 0 ]; then
	error_result "${DATETIME}" "${REPOSITORY_URL}" "0" "-" "pip3_install_-r_requirements.txt_NG"
	return 0
    fi
    docker exec ${CONTAINER_NAME} bash -c "${DO_COMMAND}"
    if [ $? -ne 0 ]; then
	error_result "${DATETIME}" "${REPOSITORY_URL}" "0" "-" "python_start.py_NG"
	return 0
    fi
    docker exec ${CONTAINER_NAME} bash -c "${POST_COMMAND}" > ${TMP_LOG}    

    # get result score
    SCORE=`cat ${TMP_LOG} | tail -1`
    echo $SCORE
    success_result ${DATETIME} ${REPOSITORY_URL} ${SCORE} ${LEVEL}
}

function do_polling(){

    ### polling ###
    # if google spread sheet will be updated
    # https://docs.google.com/forms/d/1UePTIx-ujAFulC5bRgf7OMI3u0IzzxxK2_z4NZRb1Ac/edit
    # curl https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${SHEET}?key=${API_KEY} -o ${JSONFILE}

    SPREADSHEET_ID="1LO_Vq60h5S-lBi3jETNpWrF6igMiWLJxC8vT2YZJM_0"
    SHEET="sheet1"
    API_KEY=`echo ${API_KEY}`
    JSONFILE="test.json"
    CURRENT_IDX_FILE="current_idx.txt"

    # check if updated
    curl https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${SHEET}?key=${API_KEY} -o ${JSONFILE}
    RET=$?
    if [ $RET -ne 0 ]; then
	echo "curl NG"
	error_result "-" "-" "0" "-" "curl_google_speadsheet_NG"
	return 0
    fi
    VALUE_LENGTH=`jq .values ${JSONFILE} | jq length`
    VALUE_IDX=$((VALUE_LENGTH-1))
    CURRENT_IDX="0"
    if [ -f "${CURRENT_IDX_FILE}" ]; then
	CURRENT_IDX=`cat ${CURRENT_IDX_FILE} | tail -1`
    else
	echo "please specify CURRENT_INDEX in ${CURRENT_IDX_FILE}"
	return -1
    fi

    # do tetris
    if [ "${CURRENT_IDX}" -ne "${VALUE_IDX}" ]; then
   
	for idx in `seq $((CURRENT_IDX+1)) ${VALUE_IDX}`
	do
	    ## start current idx
	    echo $idx
	    echo $idx > ${CURRENT_IDX_FILE}

	    # get time
	    # replace BLANK
	    VALUE_TIME1=`jq .values[${idx}][0] ${JSONFILE}`
	    VALUE_TIME2=${VALUE_TIME1//" "/"_"} # blank
	    VALUE_TIME=${VALUE_TIME2//"\""/""}  # "

	    # get REPOSITORY_URL
	    # DELETE unnecessary strings
	    # BLANK_CHECK:
	    # URL_CHECK: "https://github.com/seigot/tetris"
	    # CLONE tetris CHECK:
	    VALUE_URL1=`jq .values[${idx}][1] ${JSONFILE}`
	    VALUE_URL2=`echo ${VALUE_URL1} | cut -d' ' -f 1`
	    VALUE_URL=${VALUE_URL2//"\""/""}  # "
	    if [[ "$VALUE_URL" =~ "http".*"://github.com/".*"tetris" ]]; then
		echo "url string OK"
	    else
		error_result "${VALUE_TIME}" "${VALUE_URL}" "0" "1" "github_url_string_NG"
		continue
	    fi
	    git ls-remote ${VALUE_URL} > /dev/null
	    RET=$?
	    if [ $RET -ne 0 ]; then
		echo "git ls-remote NG"
		error_result "${VALUE_TIME}" "${VALUE_URL}" "0" "1" "github_url_access_NG"
		continue
	    fi

	    # get LEVEL
	    # replace double quotation
	    VALUE_LEVEL=`jq .values[${idx}][3] ${JSONFILE} | sed 's/"//g'`
	    if [ $VALUE_LEVEL == "null" ]; then
		VALUE_LEVEL=1
	    fi
	    
	    echo "LEVEL: ${VALUE_TIME}"
	    echo "URL: ${VALUE_URL}"
	    echo "LEVEL: ${VALUE_LEVEL}"

	    ## do tetris
	    do_tetris "${VALUE_TIME}" "${VALUE_URL}" "${VALUE_LEVEL}"
	done

    else
	echo "already latest version, do nothing"
    fi

    return 0
}

# while every MM minutes
while true
do
    do_polling

    if [ "${EXEC_MODE}" != "RELEASE" ];then
	echo "break polling"
	echo "  EXEC_MODE: ${EXEC_MODE}"
	break
    fi
    
    SLEEP_SEC=300
    echo "sleep: ${SLEEP_SEC}"
    sleep ${SLEEP_SEC}
done



