#!/usr/bin/php

<?php
  $url = "https://trac.rc.rit.edu/newticket";
  $username='rjbpop';
  $password='Mnlb859qaw';

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); // return into a variable
  curl_setopt($ch, CURLOPT_COOKIEJAR, '/tmp/cookies.txt');
  curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
  curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
  $result = curl_exec($ch);
  
  $pattern = '/name="__FORM_TOKEN" value="(.+?)"/';
  preg_match($pattern, $result, $matches);
  $token = $matches[1];

  $fields = array(
    'field_summary'=>'newrequest',
    'field_reporter'=>'apply2',
    'field_description'=>'description',
    'field_type'=>'task',
    'field_priority'=>'major',
    'field_milestone'=>'',
    'field_component'=>'accounts',
    'field_cc'=>urlencode('$uid@rit.edu'),
    'field_owner'=>'',
    'field_status'=>'new',
    '__FORM_TOKEN'=>$token,
  );

  $fields_string = "";
  foreach($fields as $key=>$value) {
    $fields_string .= $key.'='.$value.'&';
  }
  rtrim($fields_string,'&');
  echo "$fields_string\n\n";
  curl_setopt($ch, CURLOPT_URL, $url); // set url to post to
  curl_setopt($ch, CURLOPT_VERBOSE, true); // Display communication with server
  curl_setopt($ch, CURLOPT_FAILONERROR, 1);
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);// allow redirects
  curl_setopt($ch, CURLOPT_RETURNTRANSFER,1); // return into a variable
  curl_setopt($ch, CURLOPT_TIMEOUT, 5); // times out after 6s
  curl_setopt($ch, CURLOPT_POST, 1); // set POST method

  $username='rjbpop';
  $password='Mnlb859qaw';
  curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
  curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
  curl_setopt($ch, CURLOPT_POSTFIELDS, $fields_string);
  $result = curl_exec($ch); // run the whole process
  $info = curl_getinfo($ch);
  curl_close($ch);
  echo "result:\n";
  echo "$result\n";
  echo "info:\n";
  echo "$info\n";
  foreach($info as $key=>$value) {
      echo "$key -> $value\n";
  }

?>
