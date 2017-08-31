./main.py -X
./testing/setup.sh
echo "knewbury@ualberta.ca
crapo@ualberta.ca
" > ./config/users.txt
./main.py -t
read -p "Pausing" -t 5
echo "knewbury@ualberta.ca
crapo@ualberta.ca
hoye@ualberta.ca" > ./config/users.txt
./main.py -t
read -p "Pausing" -t 5
echo "knewbury@ualberta.ca
hoye@ualberta.ca" > ./config/users.txt
./main.py -t
read -p "Pausing" -t 5
echo "knewbury@ualberta.ca
hoye@ualberta.ca
crapo@ualberta.ca" > ./config/users.txt
./main.py -t
read -p "Pausing" -t 5
./main.py -X
