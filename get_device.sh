echo "unplug device and click enter to continue"
read cont
if [[ $cont == "" ]]; then 
    ls /dev/tty* > ./unplugged.txt
    echo "plug in device and click enter to continue"
    read cont
    if [[ $cont == "" ]]; then
        ls /dev/tty* > ./plugged.txt
        diff ./unplugged.txt ./plugged.txt > ./diff.txt
        cat ./diff.txt
        rm ./unplugged.txt ./plugged.txt ./diff.txt
    fi
fi