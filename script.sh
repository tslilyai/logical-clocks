 #!/bin/bash
for i in 10 6 4; do
    for j in $( seq 1 5 ); do
        timeout 60s python system_model.py $j $i
    done
done