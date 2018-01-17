#!/bin/bash
array=(
    'core::extBackend'
    'auth::auth-service'
    'fmgr::form-manager-service'
    'gate::api-gateway'
    'vmgr::vendormanagement'
    'wflw::workflowengine'
    'todo::todoservice'
    'ngen::numbergenerator'
    'dcmt::documentservice'
    'eprc::eprocservice'
    'dops::devopsservice'
    'tmpt::templateengineservice'
    'rept::reportingservice'
    'ctmn::catman-service'
    'c::extBackend'
    'a::auth-service'
    'f::form-manager-service'
    'g::api-gateway'
    'b::vendormanagement'
    'w::workflowengine'
    't::todoservice'
    'n::numbergenerator'
    'd::documentservice'
    'e::eprocservice'
    'o::devopsservice'
    'v::templateengineservice'
    'r::reportingservice'
    'm::catman-service'
    'mongo::mongo'
    'rmq::rmq'
    'tomcat::tomcat'
)
rmq_base_dir='/usr/local/sbin'
tomcat_base_dir='/Library/Tomcat/bin'
args=("$@")
restart=false
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
  esac  
done

function new_tab() {
  TAB_NAME=$1
  COMMAND=$2
  echo $TAB_NAME
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

for (( i=0; i < $#; ++i ))
do
  for system in "${array[@]}" ; do
  KEY="${system%%:*}"
  VALUE="${system##*:}"
  SYSTEM=${args[$i]}  
  if [[ "$KEY" == "$SYSTEM" ]]
  then
    cdto="/Users/lukas/Documents/EXT/${VALUE}/"
    if [[ "$KEY" == "mongo" ]] 
    then
      cmd="sudo mongod --config /etc/mongod.conf"
      new_tab "mongo" "$cmd"
      elif [[ "$KEY" == "rmq" ]] 
      then
        cmd="$rmq_base_dir/rabbitmq-server"
        new_tab "rabbitmq" "$cmd"
      elif [[ "$KEY" == "tomcat" ]] 
      then
        cmd="$tomcat_base_dir/startup.sh"
        new_tab "tomcat" "$cmd"
      else
        if [[ "$restart" == true ]] 
        then
          for proc in $(lsof +D ${cdto} | awk 'NR!=1 {print $2}') 
          do
            kill $proc
          done
        fi
        cmd="./gradlew bootRun"
        new_tab "${VALUE}" "cd $cdto;$cmd;"
      fi
    fi
  done
done
