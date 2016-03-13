 #!/bin/bash
for i in 0.3 0.5 0.75; do
    for j in $( seq 1 4 ); do
        timeout 60s python system_model.py $j true $i
    done
done
