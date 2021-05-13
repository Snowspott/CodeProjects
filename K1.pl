open FILE, "Org/CYS31.INP" or die $!;   #såå dette er orginal filen
@file= <FILE>;

 foreach (@file){
$a=$a+1;
}
$kk=K1;  #THE K Name
$g= 3;   #this is the Line to make the wonders inn, try to add auto system.
$max = 3.0; #this is the maxium rate abowe the $g
$jump= 0.01; #how manny jumps



$min = join('',$file[$g]);
### problem whit this, is that it dont bring a limit aria,.. ###
#### its is going from "0-(Standar+max)"###
### and i only needed somting that go from  "standar-max <-> Standar+max###
###if standar-max<0 then "standar-max"=0 ### this is important so we dont get a negative rate
### that produse an error, in the Fortran program
$b=0;
$b=$b-$min ;
$c=0;
close (FILE);

### tinking about making this sipler !
while($b <($max))  #yes there is the problem, and the fix is there to !!! ##
{

$b=(-$min)+($jump*$c);
$c=$c+1;
$f=$min+$b;
$h= $g+1;
$i= $g-1;


#this is save now
###################################################################
@hell= $file[$g] + $b;
@name = "$kk$f";
@list= (@name,"\n",@file[1..$i],@hell,"\n", @file[$h..$a]);
#################################################################
#this is safe

rename "program/CYS31.INP","CYS31.INP"; #remove old data
open (MYFILE, ">> program/CYS31.INP"); # new data
print MYFILE @list;
close (MYFILE);
system ("program/CYS33.exe"); #running new data

#This part is still unstable...
opendir(HU, ".") || print "Me Not Speek Linux/Mac";
@hu=readdir(HU);
closedir(HU);
for my $line(@hu) {
if($line =~/SCON2tot/x){
$lost1 = $line;
}
elsif($line =~/SCON2n/x){
$lost2 = $line;
}
elsif($line =~/summary/x){
$lost3 = $line;
}

$old1=$lost1;
$old2=$lost2;
$old3=$lost3;
$new1="out/$kk/RAW/$lost1";
$new2="out/Trash/$lost2";
$new3="out/$kk/Result/$lost3";
rename $old1,$new1;
rename $old2,$new2;
rename $old3,$new3;
}
open FILE, "out/$kk/Result/$lost3";
@file2= <FILE>;
close (FILE);

for my $line(@file2) {
if($line =~/age/x){
$lost4 = $line;;
}
}


$tesla = substr($lost4,23);
$tesla=~s/\s//g;


if($tesla<0.01){
print "Then i can Move som files to the Junk Factory\n";
rename $new1,$new2; #time to bring out the trash
rename $new3,$new2; #time to bring out the trash
}
else{
   if($b eq 0)
   {
   $bannan=$tesla;
   }
   else
   {
   $bannan = 0;
   }
@gnu1=($f,",","\t",$tesla,",","\t",$bannan,",","\n");  ##Add a new data line to add the normal valute
@gnuout1=(@gnuout1,@gnu1) ;


}

#Unstable part end


#if($c > 3) {exit;} #THIS IS A TESTING LINE,.. ACTIVATE WHEN DEBUG######


}


open (MYFILE, ">> out/$kk/plot.txt"); #This is the Gnuplot graf txt !
print MYFILE @gnuout1;
close (MYFILE);

exit;


