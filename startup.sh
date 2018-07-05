#!/bin/bash
array=('core::ext'
    'auth::auth-service'
    'fmgr::form-manager-service'
    'gate::api-gateway'
    'vmgr::vendormanagement'
    'wflw::workflowengine'
    'todo::todo-service'
    'ngen::numbergenerator'
    'dcmt::documentservice'
    'eprc::eprocservice'
    'dops::devopsservice'
    'tmpt::templateengineservice'
    'rept::reportingservice'
    'ctmn::catman-service'
    'clrs::clearingservice'
    'c::extBackend'
    'a::auth-service'
    'f::form-manager-service'
    'g::api-gateway'
    'b::vendormanagement'
    'w::workflowengine'
    't::todo-service'
    'n::numbergenerator'
    'd::documentservice'
    'e::eprocservice'
    'o::devopsservice'
    'v::templateengineservice'
    'r::reportingservice'
    'm::catman-service'
    's::clearingservice'
    'sr::searchservice'
    'mongo::mongo'
    'rmq::rmq'
    'elastic:elastic'
    'tomcat::tomcat')
default_services=('core::extBackend'
    'auth::auth-service'
    'fmgr::form-manager-service'
    'wflw::workflowengine'
    'todo::todoservice'
    'dcmt::documentservice')
setup=('rmq' 'mongo' 'tomcat' 'elastic' 'cerebro' 'adminmongo')

#base directories
rmq_base_dir='/usr/local/sbin'
tomcat_base_dir='/Library/Tomcat/bin'
base_dir='/Users/lukas/Documents/EXT'
mamp_base_dir='/Applications/MAMP/bin'
admin_mongo_base_dir="/Users/lukas/bin/adminMongo"
args=("$@")
restart=false

function new_tab() {
  TAB_NAME=$1
  COMMAND=$2
  osascript \
   -e "     tell application \"iTerm\"" \
   -e "     activate" \
   -e "     tell current window" \
   -e "       create tab with default profile" \
   -e "     end tell" \
   -e "     tell current tab of current window" \
   -e "       select"\
   -e "       set _session to current session" \
   -e "       tell _session" \
   -e "         write text \"$COMMAND \"" \
   -e "         set name to \"$TAB_NAME\"" \
   -e "       end tell" \
   -e "     end tell" \
   -e "   end tell"
}

function start_setup_service() {
  SERVICE_NAME=$1
  if [[ "$SERVICE_NAME" == "mongo" ]]
  then
    cmd="sudo mongod --config /etc/mongod.conf"
    new_tab "mongo" "$cmd"
  elif [[ "$SERVICE_NAME" == "rmq" ]]
  then
    echo 'starting rabbitmq...'
    cmd="$rmq_base_dir/rabbitmq-server"
    new_tab "rabbitmq" "$cmd"
  elif [[ "$SERVICE_NAME" == "tomcat" ]]
  then
    echo 'starting tomcat...'
    cmd="$tomcat_base_dir/startup.sh"
    "$cmd"
  elif [[ "$SERVICE_NAME" == "mamp" ]]
  then
    cmd="$mamp_base_dir/start.sh"
    new_tab "MAMP" "$cmd"
  elif [[ "$SERVICE_NAME" == "elastic" ]]
  then
    cmd="elastic"
    new_tab "elasticsearch" "$cmd"
  elif [[ "$SERVICE_NAME" == "cerebro" ]]
  then
    cmd="cerebro"
    new_tab "cerebro" "$cmd"
  elif [[ "$SERVICE_NAME" == "adminmongo" ]]
  then
    cmd="cd $admin_mongo_base_dir && npm start"
    new_tab "adminmongo" "$cmd"
  fi
}

for var in "$@"
do
  case $var in
    --i|--info)
    for service in "${array[@]}"
    do
      echo $service
    done
    shift
    ;;
    --r|--restart)
    restart=true
    ;;
    --d|--default)
    for service in "${default_services[@]}"
    do
      KEY="${service%%:*}"
      VALUE="${service##*:}"
      cdto="${base_dir}/${VALUE}/"
      cmd="./gradlew bootRun"
      new_tab "${VALUE}" "cd $cdto;$cmd;"
    done
    ;;
    --s|--setup)
    for service in "${setup[@]}"
    do
      start_setup_service "$service"
    done
  esac
done

for (( i=0; i < $#; ++i ))
do
  for system in "${array[@]}" ; do
    KEY="${system%%:*}"
    VALUE="${system##*:}"
    SYSTEM=${args[$i]}
    LANGDIR="/data1/ext/lang"
    if [[ "$KEY" == "$SYSTEM" ]]
    then
      cdto="${base_dir}/${VALUE}/"
      if [[ "$restart" == true ]]
      then
        for proc in $(lsof +D ${cdto} | awk 'NR!=1 {print $2}')
        do
          kill $proc
        done
      fi
      if [[ "$VALUE" == "extBackend" ]]
      then
        if [[ ! -d "$LANGDIR" ]]
        then
          mkdir -p "$LANGDIR"
        fi
        cp -r "${cdto}grails-app/conf/lang/" "${LANGDIR}/"
      fi
      cmd="./gradlew bootRun"
      new_tab "${VALUE}" "cd $cdto;$cmd;"
    fi
  done
done
