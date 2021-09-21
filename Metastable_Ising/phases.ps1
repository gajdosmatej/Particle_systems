#LANG=en_US
#parametry: L = 20 N_steps = 800000

for($B = 3.3; $B -lt 10; $B = $B + 0.1){
	for($A = 0.14; $A -lt 0.2; $A = $A + 0.01){
        	Write-Host A$A B$B
        	py simulate.py $A $B
        	py calc_E.py $A $B

	}
}
