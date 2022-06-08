#This code will create a directory inside your colab space, and then link it with the cloud storage

!echo deb http://packages.cloud.google.com/apt gcsfuse-bionic main > /etc/apt/sources.list.d/gcsfuse.list
!curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
!apt -qq update
!apt -qq install gcsfuse
!mkdir colab_direct
!gcsfuse --implicit-dirs urbanforest colab_direct

#Then saving a csv file into the colab_direct will make it also appear in the cloud storage

data.to_csv("colab_direct/dataFileName.csv", index=False)
