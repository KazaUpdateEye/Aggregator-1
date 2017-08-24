file="/home/Videos/5c089768-958a-4a46-abda-9265ed91a35d/304d095f-7539-416a-9d86-f6a02dd4ba8c/Hybrid/fffe00d8-bf10-40e6-8cf6-659b1b47fd90.avi"
$fileUnixTimeDate = filemtime ( $file );
$todayUnixTimeDate =  time();
$unixDifference = $todayUnixTimeDate - $fileUnixTimeDate;
$daysDifference = $unixDifference/86400;
echo $daysDifference
