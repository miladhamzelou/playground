#!/bin/bash
get_current_height(){
    IP=$1
    PORT=$2
    if [ ! -n "$IP" ]; then
	IP="127.0.0.1"
    fi
    if [ ! -n "$PORT" ]; then
	PORT=46657
    fi
    response=`curl -s ${IP}:${PORT}/status | grep 'latest_block_height' | sed 's/\"//g'`
    if [ $? -ne 0 ]; then
	exit 1
    fi
    height=`echo ${response} | grep -o '[0-9]\+'`
    echo $((height))
    return 0
}

get_height(){
    if [ $# -ne 3 ]; then
	echo -e " Syntax Error:Wrong number of arguments!\n"
	exit 1
    fi
    
    IP=$1
    PORT=$2
    timeout=$3
    start=$(date +%s)

    while [ 1 ]; do
	height=$( get_current_height ${IP} ${PORT})
	if [ $? -eq 0 ]; then
	echo ${height}
	return 0
	fi
   
	now=$(date +%s)
	
	if [ $((now-start-timeout)) -gt 0 ]; then
	    echo "TIMEOUT: ${timeout}!\n"
	    return 1
	fi
	sleep 1
    done
    echo -e "WRONG!\n"
    return 1
}

check_height_growth(){
    if [ $# -ne 3 ]; then
	echo -e "Syntax Error:Wrong number arguments!\n"
	return 1
    fi
    
    IP=$1
    PORT=$2
    Timeout=$3

    oldHeight=$( get_height ${IP} ${PORT} ${Timeout})
    if [[ $? -ne 0 ]]; then
	echo -e "Failed to get oldHeight!\n"
	return 1
    fi

    #echo -e "OldHeight = ${oldHeight}\n"
    startTime=$(date +%s)
    while [ 1 ];do
	newHeight=$( get_height ${IP} ${PORT} ${Timeout} )
	if [[ $? -ne 0 ]];then
	    echo -e "Failed to get newHeight!\n"
	    return 1
	fi

	currentTime=$(date +%s)
	if [ ${newHeight} -gt ${oldHeight} ]; then
	    #echo -e "NewHeight = ${newHeight}\n"
	    echo "$((currentTime - startTime))"
	    return 0
	fi

	if [ $((currentTime - startTime)) -gt ${Timeout} ]; then
	    echo -e "Timeout:${Timeout}"
	    return 20
	fi
	sleep 1
    done
    return 1
}
check_height_growth_normal(){
    if [ $# -ne 3 ]; then
	echo -e "Syntax Error:Wrong number arguments!\n"
	return 1
    fi
    
    IP=$1
    PORT=$2
    Timeout=$3
    
    startTime=$(date +%s)
    for i in {0..1}; do
	Message=$(check_height_growth ${IP} ${PORT} ${Timeout})
	if [ $? -ne 0 ]; then
	    echo -e "Filed to check_height_growth ${IP} ${PORT} ${Timeout}\n"
	    return 1
	fi
	
	if [[ ${Message} -lt ${Timeout} ]]; then
	    currentTime=$(date +%s)
	    echo "$((currentTime-startTime))"
	    return 0
	fi
    done
    echo -e "Block height growth time(${Message}) > timeout(${Timeout})\n"
    return 1
}
