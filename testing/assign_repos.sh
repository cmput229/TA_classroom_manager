./main.py -X
./testing/setup.sh
echo "knewbury@ualberta.ca
crapo@ualberta.ca
" > ./config/users.txt
./main.py -t
./main.py -R lab1 -d
./main.py -R lab3 -d
read -p "Pausing" -t 5
echo ""
echo "knewbury@ualberta.ca
crapo@ualberta.ca
hoye@ualberta.ca" > ./config/users.txt
./main.py -t
read -p "Pausing" -t 5
echo ""
./main.py -X
