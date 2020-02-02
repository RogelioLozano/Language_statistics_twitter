#!/bin/bash
#SBATCH -n 1
#SBATCH -o salidaST1.un
#SBATCH -e errorST1.un
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=rogelio97@ciencias.unam.mx


cd $HOME/Datos_correctos/scripts_nuevos && python contartweets.py
