import vk_api, yandex_music, time, threading, json, logging
from vk_api.longpoll import VkLongPoll, VkEventType
from yandex_music.client import Client
from threading import Thread

# Отключаем логгирование ошибок
logger = logging.getLogger('yandex_music')
logger.setLevel(logging.ERROR)

def open_config():
	with open("config.json", encoding="utf-8") as config_file:
		return json.load(config_file)

config = open_config()

# Параметры для входа.
vk_id = config[0]["vk_id"]
vk_token = config[0]["vk_token"]

# Команды.
statusUpdate = config[2]["statusUpdate"]
startSymbolUpdate = config[2]["startSymbolUpdate"]
endSymbolUpdate = config[2]["endSymbolUpdate"]

# Авторизация в Яндекс Музыке
client = Client.from_credentials(config[0]["yandexLogin"], config[0]["yandexPassword"])

# Авторизация во вконтакте.
vkSession = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vkSession)
vk = vkSession.get_api()

# Временные переменные (нужны для обхода капчи и смены статуса на обычный, если музыка осталась той же).
lastSong = 0
lastSongName = ""
afk = False

# Обработчик команд в вк.
def commandChecker():
	for event in longpoll.listen():
		try:
			if event.type == VkEventType.MESSAGE_NEW:
				if event.user_id == vk_id:
					if event.message.lower().startswith(statusUpdate):
						loaded_config = open_config()
						loaded_config[1]["status"] = event.message[len(statusUpdate) + 1:]
						with open("config.json", "w", encoding="utf-8") as config_dump_out:
							json.dump(loaded_config, config_dump_out, indent=2, ensure_ascii=False)
						statusUpdateText = "⚙|Статус был успешно обновлён!"
						vk.messages.edit(peer_id=event.peer_id, message=statusUpdateText, message_id=event.message_id)
						time.sleep(3)
						vk.messages.delete(message_ids=event.message_id, delete_for_all=1)
					if event.message.lower().startswith(startSymbolUpdate):
						loaded_config = open_config()
						loaded_config[1]["startSymbol"] = event.message[len(startSymbolUpdate)+1:]
						print(loaded_config)
						with open("config.json", "w", encoding="utf-8") as config_dump_out:
							json.dump(loaded_config, config_dump_out, indent=2, ensure_ascii=False)
						startSymbolUpdateText = "⚙|Символы в начале статуса были успешно обновлены!"
						vk.messages.edit(peer_id=event.peer_id, message=startSymbolUpdateText, message_id=event.message_id)
						time.sleep(3)
						vk.messages.delete(message_ids=event.message_id, delete_for_all=1)
					if event.message.lower().startswith(endSymbolUpdate):
						loaded_config = open_config()
						loaded_config[1]["endSymbol"] = event.message[len(endSymbolUpdate)+1:]
						with open("config.json", "w", encoding="utf-8") as config_dump_out:
							json.dump(loaded_config, config_dump_out, indent=2, ensure_ascii=False)
						endSymbolUpdateText = "⚙|Символы в начале статуса были успешно обновлены!"
						vk.messages.edit(peer_id=event.peer_id, message=endSymbolUpdateText, message_id=event.message_id)
						time.sleep(3)
						vk.messages.delete(message_ids=event.message_id, delete_for_all=1)
		except Exception as logError:
			print(f"Ошибка в цикле для обработки команд!\n{logError}")
			continue

Thread(target=commandChecker, name="check_commands").start()

# Цикл, находящий воспроизводимую в текущий момент песню и ставящий её в статус.
# Дополнительно обновляет переменные с параметрами, изменёнными с помощью команд
while True:
	try:
		# Блок для обновления изменяемых параметров
		config = open_config()
		startSymbol = config[1]["startSymbol"]
		endSymbol = config[1]["endSymbol"]
		afkTime = config[1]["afkTime"]
		status = config[1]["status"]

		# Блок, который находит песню, воспроизводимую в текущий момент.
		queue_id = client.queues_list()[0]['context']['id'] # Находим играющую очередь и её id.
		trackIndex = client.queue(queue_id=client.queues_list()[0].id).current_index # Находим индекс воспроизводимого трека в очереди.
		trackID = client.queue(queue_id=client.queues_list()[0].id).tracks[trackIndex] # Находим айди воспроизводимого трека.
		getTrackInfo = client.tracks([f"{trackID['track_id']}:{trackID['album_id']}"]) # Получаем необходимую информацию о треке.
		trackArtists = []

		# Складываем всех исполнителей трека в одну строку (если он один, то просто превращаем в строку).
		for elem in getTrackInfo[0]['artists']:
			trackArtists.append(elem['name'])
		trackArtists = ', '.join(trackArtists)

		# Находим название песни.
		trackTitle = getTrackInfo[0]['title']

		# Складываем весь текст статуса, вместе с символами.
		trackFullName = f"{startSymbol}{trackArtists} — {trackTitle}{endSymbol}"

		# Фильтрация на повторные треки (если трек другой, обнуляется временная переменная,
		# ставится статус, а если афк-режим был включён, то выключает его.
		if trackFullName != lastSongName:
			lastSongName = trackFullName
			lastSong = 1
			vk.status.set(text=trackFullName)
			if afk == True:
				afk = False

		# Если же трек тот же, то заполняет временную переменную с каждой итерацией на одно число.
		# Итерации происходят с периодичностью в 10 секунд, соответственно, время для афк-режима поэтому и делится на 10.
		else:
			lastSong += 1

		# Если количество итераций превышает заданное, а т.е. один трек висит больше указанного времени,
		# то возвращается прежний статус, а афк-режим включается.
		if lastSong > afkTime:
			if afk == False:
				vk.status.set(text=status)
				afk = True
		time.sleep(10)
	except Exception as logError:
		print(f"Ошибка в цикле для нахождения трека!\n{logError}")
		continue