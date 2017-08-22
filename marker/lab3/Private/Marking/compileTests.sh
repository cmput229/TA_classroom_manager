rm -f tests/*.bin
for f in tests/*.s
do
echo "Compiling $f ..."
echo -n "	"
expect assemble.exp $f ${f%.s}.bin | sed '1,7d' | sed '2d'
done
