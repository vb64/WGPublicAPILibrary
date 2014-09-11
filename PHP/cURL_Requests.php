<?php
$url = "http://api.worldofwarplanes.ru/wowp/account/info/"; //URl запроса
$application_id = 'demo'; //Application ID WG
$language = 'ru'; //Язык ответа от API
$user_id_array = array('account_id', 'account_id'); //Список Account ID пользователей

$field = "application_id=" . $application_id . "&language=" . $language . "&account_id=" . implode(",", $user_id_array);

$ch = curl_init(); //Инициализирует сеанс cURL
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $field);

$try = 0; //Счетчик количества повторов получения данных
$baseT = 10; // базовый таймаут в секундах

do {
  $data = curl_exec($ch); //Делаем запрос к API
  $response = json_decode($data, true); //Декодирует JSON строку
  $try++; // Увеличиваем значение счетчика
  
  if ((!empty(curl_errno($ch))) || (empty($response)))
  {
    sleep( $baseT + (($try-1*5))); //если ошибка, увелиить интервал
  }
  
}  while (curl_errno($ch) and $try < 10 and $response['status'] != 'ok'); //Проверяем что запрос к апи успешно прошел, и устанавливаем лимит не более 10 запросов к API

curl_close($ch); //Завершает сеанс cURL

foreach ($response as $key => $value) {
    if (is_array($value)) { //Если значение масив проходим по внутренему массиву
        echo "Ключ = " . $key . " Значение = " . $value;
        foreach ($value as $sub_key => $sub_value) {
            echo "Ключ 2 уровня= " . $sub_key . " Значение 2 уровня = " . $sub_value;
        }
    } else {
        echo "Ключ = " . $key . " Значение = " . $value;
    }
}
