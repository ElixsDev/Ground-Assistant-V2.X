python cli.py --start
sleep 10
python cli.py --stop #| read varstop
python cli.py --status #| read varstatus
python cli.py --continue #| read varcontinue
python cli.py --restart #| read varrestart
python cli.py --refresh_ndb #| read varndb
python cli.py --status #| read varstatus2
python cli.py --close #| read $varclose

#if [ "$varstart" = "Started Ground-Assistant." ]
#then
#    echo Start: Passed
#else
#    echo $varstart
#fi
#if [ "$varclose" = "Sent close." ]
#then
#    echo Close: Passed
#else
#    echo $varclose
#fi
