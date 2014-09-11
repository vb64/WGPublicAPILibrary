<?php
// Примерный код
//Получение основной информации про танки

//инициация HTTP-клиента
$client = new Zend_Http_Client();

//установка URI базового
$client->setUri('http://api.worldoftanks.ru/wot/encyclopedia/tanks/');

//Установка опций
$client->setConfig(array(
    'maxredirects' => 1,
    'timeout'      => 30, //таймаут на запросы
		'useragent' => 'Test Server API/PHP 5.5',
		'keepalive' => true  //если вы хотите еще делать запросы, то для улучшения быстродействия установить в true
));
	
//выставляем нужные параметры авторизации
$client->setParameterGet(array(
  'application_id'  => '<ВАШ КЛЮЧ АВТОРИЗАЦИИ>',
  'language' => 'ru'
));

//делаем запрос
$response = $client->request('GET');

//обработка результата - сначала проверим фактическую успешность HTTP-запроса
if (  $response->isSuccessful() )
{
	echo "Request successful...\n";
		
	//получим тело ответа в раскодированой форме
	$_data = $response->getBody();
		
	//преобразуем в ассоциативный массив
	$data = Zend_Json::decode( $_data );
		
	if (($data['status'] == 'ok') && (!empty($data['data'])))
	{
		foreach($data['data'] as $t)
		{
		
		  //здесь имеем информацию про танки и обрабатываем ее
		  
		  
		}
	}
	else
			echo "[ERROR] API Request error: " . $data['error']['message'] . "\n";
}
else
    echo "[ERROR] API Request HTTP error \n";
    
    
  
