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

    local DATETIME="$1" #`date +%Y%m%d_%H%M_%S`
    local REPOSITORY_URL="$2"
    local BRANCH="$3"
    local SCORE="$4"
    local LEVEL="$5"
    local RESULT="$6"
    local DROP_INTERVAL="$7"
    local VALUE_MODE="$8"
    local VALUE_PREDICT_WEIGHT="$9"
    local LINE1_SCORE="${10}"
    local LINE2_SCORE="${11}"
    local LINE3_SCORE="${12}"
    local LINE4_SCORE="${13}"
    local GAMEOVER_SCORE="${14}"
    local DROPDOWN_SCORE="${15}"
    local BLOCK_NO="${16}"
    local TRIAL_NUM="${17}"
    local SCORE_MEAN="${18}"
    local SCORE_STDEV="${19}"
    local SCORE_MAX="${20}"
    local SCORE_MIN="${21}"

    local HEADER_STR="DATETIME, REPOSITORY_URL, BRANCH, SCORE, LEVEL, RESULT, DROP_INTERVAL, VALUE_MODE, VALUE_PREDICT_WEIGHT, 1LINE_SCORE, 2LINE_SCORE, 3LINE_SCORE, 4LINE_SCORE, GAMEOVER_SCORE, DROPDOWN_SCORE, BLOCK_NO, TRIAL_NUM, SCORE_MEAN, SCORE_STDEV, SCORE_MAX, SCORE_MIN"
    local STR="${DATETIME}, ${REPOSITORY_URL}, ${BRANCH}, ${SCORE}, ${LEVEL}, ${RESULT}, ${DROP_INTERVAL}, ${VALUE_MODE}, ${VALUE_PREDICT_WEIGHT}, ${LINE1_SCORE}, ${LINE2_SCORE}, ${LINE3_SCORE}, ${LINE4_SCORE}, ${GAMEOVER_SCORE}, ${DROPDOWN_SCORE}, ${BLOCK_NO}, ${TRIAL_NUM}, ${SCORE_MEAN}, ${SCORE_STDEV}, ${SCORE_MAX}, ${SCORE_MIN}"

    ## update result file
    local RESULT_LOG="result.csv"
    local RESULT_LEVEL_LOG="result_level_${LEVEL}.csv"
    local RESULT_RANKING_LOG="result_ranking_level_${LEVEL}.csv"

    if [ ! -e ${RESULT_LOG} ]; then
	echo "${HEADER_STR}" >> ${RESULT_LOG}
    fi
    echo $STR >> ${RESULT_LOG}

    if [ "${RESULT}" == "SUCCESS" ]; then
	if [ ! -e ${RESULT_LEVEL_LOG} ]; then
	    echo "${HEADER_STR}" >> ${RESULT_LEVEL_LOG}
	fi
	echo $STR >> ${RESULT_LEVEL_LOG}
	cat <(head -1 ${RESULT_LEVEL_LOG}) <(tail -n +2 ${RESULT_LEVEL_LOG} | sort -nr -t, -k4) > ${RESULT_RANKING_LOG}
    fi
	
    echo "--"
    cat ${RESULT_LOG}
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
    ##  - result*.log
    ##  - detail/*.json
    ##
    #git clone https://github.com/seigot/tetris_score_server
    #pushd tetris_score_server/logs
    DETAIL_LOGDIR_NAME="detail"
    git pull
    git add ${RESULT_LOG}
    git add ${RESULT_LEVEL_LOG}
    git add ${RESULT_RANKING_LOG}
    git add ${DETAIL_LOGDIR_NAME}/*.json
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
    update_result "$1" "$2" "$3" "$4" "$5" "$6" "$7" "${8}" "${9}" "-" "-" "-" "-" "-" "-" "-" "-" "-" "-" "-" "-"
}

function success_result(){

    #DATETIME="$1" #`date +%Y%m%d_%H%M_%S`
    #REPOSITORY_URL="$2"
    #SCORE="$3"
    #LEVEL="$4"
    #STR="${DATETIME}, ${REPOSITORY_URL}, ${SCORE}, ${LEVEL}, SUCCESS"
    #update_result "${STR}"
    update_result "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}" "${18}" "${19}" "${20}" "${21}"
}

function check_drop_interval_value(){

    input=${1}
    # check if input is int
    # 0: 式が正しく評価され、評価値が0かnull以外の場合
    # 1: 式が正しく評価され、評価値が0かnullのとき
    # 2: 式が不当なとき
    # 3: (GNU版のみ)その他エラーが起こったとき
    expr "$input" + 0 >&/dev/null
    ret=$?
    if [ $ret -lt 2 ];then
        echo "$input is an int number: ${ret}"
    else
        echo "$input is not an int number: ${ret}"
        return 1
    fi

    # check if larget than 0
    if [ $input -gt 0 ];then
        echo "$input is in correct range."
    else
        echo "$input is invalid range."
        return 1
    fi

    return 0
}

function do_tetris(){

    # parameter declaration
    local DATETIME="$1"
    local REPOSITORY_URL="$2"
    local BRANCH="$3"
    local LEVEL="$4"
    local DROP_INTERVAL="$5"
    local VALUE_MODE="$6"
    local VALUE_PREDICT_WEIGHT="$7"

    local GAME_TIME="180"
    if [ "${EXEC_MODE}" != "RELEASE" ]; then
	GAME_TIME="3" # debug value
    fi

    local RESULT_JSON="result.json"
    local PRE_COMMAND="cd ~ && rm -rf tetris && git clone ${REPOSITORY_URL} -b ${BRANCH} && cd ~/tetris && pip3 install -r requirements.txt"
    local DO_COMMAND="cd ~/tetris && export DISPLAY=:1 && python3 start.py -l ${LEVEL} -t ${GAME_TIME} -d ${DROP_INTERVAL} -m ${VALUE_MODE} --predict_weight ${VALUE_PREDICT_WEIGHT} && jq . ${RESULT_JSON}"
    local POST_COMMAND="cd ~/tetris && jq . ${RESULT_JSON}"

    local TMP_LOG="tmp.json"
    local TMP2_LOG="tmp2.log"
    local OUTPUTJSON="output.json"
    local CONTAINER_NAME="tetris_docker"

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
	error_result "${DATETIME}" "${REPOSITORY_URL}" "${BRANCH}" "0" "${LEVEL}" "pip3_install_-r_requirements.txt_NG" "${DROP_INTERVAL}" "${VALUE_MODE}" "${VALUE_PREDICT_WEIGHT}"
	return 0
    fi
    docker network disconnect bridge ${CONTAINER_NAME}

    # exec loop
    local LOOP_MAX=10
    local SCORE_MAX=-10000000000
    local SCORE_MAX_INDEX=1
    local SCORE_ARRAY=()
    echo {} | jq . > ${OUTPUTJSON}
    for N in `seq 1 ${LOOP_MAX}`; do    
	# do command
	rm -rf ${TMP_LOG}
	docker exec ${CONTAINER_NAME} bash -c "${DO_COMMAND}"
	if [ $? -ne 0 ]; then
	    # check score not to get value successfully.."cd ~/tetris && jq . ${RESULT_JSON}"
	    docker exec ${CONTAINER_NAME} bash -c "${POST_COMMAND}" > ${TMP_LOG}
	    CURRENT_SCORE=`jq .judge_info.score ${TMP_LOG}`
	    if [ "${CURRENT_SCORE}" == "0" -o "${CURRENT_SCORE}" == "" ]; then
		echo "end with error.."
		error_result "${DATETIME}" "${REPOSITORY_URL}" "${BRANCH}" "0" "${LEVEL}" "python_start.py_NG" "${DROP_INTERVAL}" "${VALUE_MODE}" "${VALUE_PREDICT_WEIGHT}"
		return 0
	    fi
	    echo "skip error, maybe okay."
	fi
	# get result
	docker exec ${CONTAINER_NAME} bash -c "${POST_COMMAND}" > ${TMP_LOG}

	# check if max score
	CURRENT_SCORE=`jq .judge_info.score ${TMP_LOG}`
	if [ ${CURRENT_SCORE} -ge ${SCORE_MAX} ];then
            SCORE_MAX=${CURRENT_SCORE}
            SCORE_MAX_INDEX=${N}
        fi
	SCORE_ARRAY+=("${CURRENT_SCORE}")

	# merge result to ${OUTPUTJSON}
	RESULT_JSON_STR=`jq . ${TMP_LOG}`
	jq ".index${N} = ${RESULT_JSON_STR}" ${OUTPUTJSON} > tmp && mv tmp ${OUTPUTJSON}

	# store log result
	DETAIL_LOGDIR_NAME="detail"
	mkdir -p ${DETAIL_LOGDIR_NAME}
	LOGNAME="${DATETIME}_${REPOSITORY_URL}_${BRANCH}_${LEVEL}_${DROP_INTERVAL}_${VALUE_MODE}_${VALUE_PREDICT_WEIGHT}_${N}.json"
	LOGNAME_MOD=`echo ${LOGNAME} | tr '/' '_'`
	cp ${TMP_LOG} ${DETAIL_LOGDIR_NAME}/${LOGNAME_MOD}
    done

    # get result score
    SCORE=`jq .index${SCORE_MAX_INDEX}.judge_info.score ${OUTPUTJSON}`
    echo $SCORE
    STAT_LINE1=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score_stat[0] ${OUTPUTJSON}`
    LINE1=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score.line1 ${OUTPUTJSON}`
    STAT_LINE2=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score_stat[1] ${OUTPUTJSON}`
    LINE2=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score.line2 ${OUTPUTJSON}`
    STAT_LINE3=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score_stat[2] ${OUTPUTJSON}`
    LINE3=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score.line3 ${OUTPUTJSON}`
    STAT_LINE4=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score_stat[3] ${OUTPUTJSON}`
    LINE4=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score.line4 ${OUTPUTJSON}`
    STAT_GAMEOVER=`jq .index${SCORE_MAX_INDEX}.debug_info.line_score.gameover ${OUTPUTJSON}`
    GAMEOVER=`jq .index${SCORE_MAX_INDEX}.judge_info.gameover_count ${OUTPUTJSON}`
    BLOCK_NO=`jq .index${SCORE_MAX_INDEX}.judge_info.block_index  ${OUTPUTJSON}`

    LINE1_SCORE=$(( STAT_LINE1 * LINE1 ))
    LINE2_SCORE=$(( STAT_LINE2 * LINE2 ))
    LINE3_SCORE=$(( STAT_LINE3 * LINE3 ))
    LINE4_SCORE=$(( STAT_LINE4 * LINE4 ))
    GAMEOVER_SCORE=$(( STAT_GAMEOVER * GAMEOVER ))
    DROPDOWN_SCORE=$(( SCORE - LINE1_SCORE - LINE2_SCORE - LINE3_SCORE - LINE4_SCORE - GAMEOVER_SCORE ))
    # get statistics value
    echo ${SCORE_ARRAY[@]} | python3 get_statistics.py > ${TMP2_LOG}
    TRIAL_NUM=`cat ${TMP2_LOG} | grep "num" | cut -d' ' -f2`
    MEAN=`cat ${TMP2_LOG} | grep "mean" | cut -d' ' -f2`
    STDEV=`cat ${TMP2_LOG} | grep "stdev" | cut -d' ' -f2`
    MAX=`cat ${TMP2_LOG} | grep "max" | cut -d' ' -f2`
    MIN=`cat ${TMP2_LOG} | grep "min" | cut -d' ' -f2`

    success_result "${DATETIME}" "${REPOSITORY_URL}" "${BRANCH}" "${SCORE}" "${LEVEL}" "SUCCESS" "${DROP_INTERVAL}" "${VALUE_MODE}" "${VALUE_PREDICT_WEIGHT}" "${LINE1_SCORE}" "${LINE2_SCORE}" "${LINE3_SCORE}" "${LINE4_SCORE}" "${GAMEOVER_SCORE}" "${DROPDOWN_SCORE}" "${BLOCK_NO}" "${TRIAL_NUM}" "${MEAN}" "${STDEV}" "${MAX}" "${MIN}"
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
	error_result "-" "-" "-" "0" "-" "curl_google_speadsheet_NG" "-" "-" "-"
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
	    # CLONE tetris, and branch CHECK:
	    VALUE_URL1=`jq .values[${idx}][1] ${JSONFILE}`
	    VALUE_URL2=`echo ${VALUE_URL1} | cut -d' ' -f 1`
	    VALUE_URL=${VALUE_URL2//"\""/""}  # "
	    if [[ "$VALUE_URL" =~ "http".*"://github.com/".*"tetris"$ ]]; then
		echo "url string OK"
	    else
		error_result "${VALUE_TIME}" "${VALUE_URL}" "-" "0" "-" "github_url_string_NG" "-" "-" "-"
		continue
	    fi
	    git ls-remote ${VALUE_URL} > /dev/null
	    RET=$?
	    if [ $RET -ne 0 ]; then
		echo "git ls-remote NG"
		error_result "${VALUE_TIME}" "${VALUE_URL}" "-" "0" "-" "github_url_access_NG" "-" "-" "-"
		continue
	    fi
	    VALUE_BRANCH=`jq .values[${idx}][4] ${JSONFILE} | sed 's/"//g'`
	    if [ "$VALUE_BRANCH" == "null" -o "${VALUE_BRANCH}" == "" ]; then
		echo "use default BRANCH"
		VALUE_BRANCH="master"
	    fi
	    git ls-remote ${VALUE_URL} | cut -f 2 | cut -d/ -f 3 | grep --line-regexp "${VALUE_BRANCH}"
	    RET=$?
	    if [ $RET -ne 0 ]; then
		echo "git ls-remote NG"
		error_result "${VALUE_TIME}" "${VALUE_URL}" "${VALUE_BRANCH}" "0" "-" "github_url_branch_access_NG" "-" "-" "-"
		continue
	    fi

	    # get LEVEL
	    # replace double quotation
	    VALUE_LEVEL=`jq .values[${idx}][3] ${JSONFILE} | sed 's/"//g'`
	    if [ "$VALUE_LEVEL" == "null" ]; then
		VALUE_LEVEL=1
	    fi

	    # get DROP_INTERVAL
	    VALUE_DROP_INTERVAL=`jq .values[${idx}][5] ${JSONFILE} | sed 's/"//g'`
	    if [ "$VALUE_DROP_INTERVAL" == "null" -o "${VALUE_DROP_INTERVAL}" == "" ]; then
		echo "use default VALUE_DROP_INTERVAL"
		VALUE_DROP_INTERVAL=1000
	    fi
	    check_drop_interval_value ${VALUE_DROP_INTERVAL}
	    RET=$?
	    if [ $RET -ne 0 ]; then
		echo "check_drop_interval_valuegit NG"
		error_result "${VALUE_TIME}" "${VALUE_URL}" "${VALUE_BRANCH}" "0" "-" "check_drop_interval_value_NG" "${VALUE_DROP_INTERVAL}" "-" "-"
		continue
	    fi	    

	    # get MODE(predict,predict_sample,predict_sample2)
	    VALUE_MODE=`jq .values[${idx}][6] ${JSONFILE} | sed 's/"//g'`
	    if [ "$VALUE_MODE" == "null" -o "${VALUE_MODE}" == "" ]; then
		echo "use default VALUE_MODE"
		VALUE_MODE="default"
	    fi

	    # get PREDICT_WEIGHT
	    VALUE_PREDICT_WEIGHT=`jq .values[${idx}][8] ${JSONFILE} | sed 's/"//g'`
	    if [ "$VALUE_PREDICT_WEIGHT" == "null" -o "${VALUE_PREDICT_WEIGHT}" == "" ]; then
		echo "use default VALUE_PREDICT_WEIGHT"
		VALUE_PREDICT_WEIGHT="outputs/latest/best_weight.pt"
	    fi
	    
	    echo "TIME: ${VALUE_TIME}"
	    echo "URL: ${VALUE_URL}"
	    echo "BRANCH: ${VALUE_BRANCH}"
	    echo "LEVEL: ${VALUE_LEVEL}"
	    echo "VALUE_DROP_INTERVAL: ${VALUE_DROP_INTERVAL}"
	    echo "VALUE_MODE: ${VALUE_MODE}"
	    echo "VALUE_PREDICT_WEIGHT: ${VALUE_PREDICT_WEIGHT}"

	    ## do tetris
	    do_tetris "${VALUE_TIME}" "${VALUE_URL}" "${VALUE_BRANCH}" "${VALUE_LEVEL}" "${VALUE_DROP_INTERVAL}" "${VALUE_MODE}" "${VALUE_PREDICT_WEIGHT}"
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



