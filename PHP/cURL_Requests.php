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

$response = json_decode(curl_exec($ch), true); //Декодирует JSON строку
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
