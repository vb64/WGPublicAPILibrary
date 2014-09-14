using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

// Требуется подключить Newtonsoft.Json (Json.NET)
using Newtonsoft.Json.Linq;


// Автор: IzeBerg
// Спасибо vb64 за описание структуры реплеев
namespace RepalysParser
{
    class Program
    {
        public static string PackedFileName = null, PackedFilePath = null;
        public static long ReplaySign = 288633362;

        static void Main(string[] args)
        {
            int CountFiles = args.Count();
            if (CountFiles != 0)
            {
                string file = null;
                for (int i = 0; i < CountFiles; i++)
                {
                    file = args[i];

                    PackedFileName = Path.GetFileName(file).ToLower();
                    PackedFilePath = Path.GetFullPath(file).ToLower();

                    Console.WriteLine(PackedFileName + " чтение...");
                    FileStream FS = null;
                    try
                    {
                        FS = new FileStream(file, FileMode.Open, FileAccess.Read);

                        // Читаем сигнатуру файла .wotreplay
                        Byte[] sign_buffer = new Byte[4];
                        FS.Read(sign_buffer, 0, sign_buffer.Length);
                        int file_sign = BitConverter.ToInt32(header_buffer, 0);

                        // Проверяем сигнатуру
                        if (file_sign == ReplaySign)
                        {
                            Console.WriteLine(PackedFileName + " получение данных...");

                            // Проверка есть-ли релуьтаты боя
                            bool isBattleEnd = false;
                            Byte[] isBattleEnd_buffer = new Byte[4];
                            FS.Read(isBattleEnd_buffer, 0, isBattleEnd_buffer.Length);
                            if (BitConverter.ToInt32(isBattleEnd_buffer, 0) == 2) isBattleEnd = true;

                            // Длина блока начальных уловий боя
                            Byte[] json1_count_buffer = new Byte[4];
                            FS.Read(json1_count_buffer, 0, json1_count_buffer.Length);
                            int json1_count = BitConverter.ToInt32(json1_count_buffer, 0);

                            // Читаем блок начальных уловий боя
                            Byte[] json1_buffer = new Byte[json1_count];
                            FS.Read(json1_buffer, 0, json1_count);
                            string json1 = Encoding.ASCII.GetString(json1_buffer);
                            JObject json1_obj = JObject.Parse(json1);

                            JArray json2_obj;
                            string json2 = null;
                            if (isBattleEnd)
                            {
                                // Длинна результатов боя
                                Byte[] json2_count_buffer = new Byte[4];
                                FS.Read(json2_count_buffer, 0, json2_count_buffer.Length);
                                int json2_count = BitConverter.ToInt32(json2_count_buffer, 0);

                                // Читаем результаты боя
                                Byte[] json2_buffer = new Byte[json2_count];
                                FS.Read(json2_buffer, 0, json2_count);
                                json2 = Encoding.ASCII.GetString(json2_buffer);
                                json2_obj = JArray.Parse(json2);
                            }
                            else json2_obj = new JArray();

                            JObject json = new JObject();
                            json.Add("BattleStart", json1_obj); // Блок с начальными условиями боя
                            json.Add("isBattleEnded", isBattleEnd); // Булевое значение, если true - секция BattleEnd не пустое
                            json.Add("BattleEnd", json2_obj); // Блок с результатами боя, если такового нет - пустое

                            File.WriteAllText(PackedFileName + ".json", json.ToString());
                            Console.WriteLine("Сохранено в " + PackedFileName);
                        }
                        else
                            Console.WriteLine(PackedFileName + " не реплей!");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                    finally
                    {
                        try
                        {
                            FS.Close();
                        }
                        catch { }
                    }
                }
            }
            else
            {
                Console.WriteLine("Используйте 'Открыть с помощью..' или комманду '<unpacker_path> <replay_path>' для парсинга реплея.");
            }
            
            Console.WriteLine("Парсинг реплеев завершен, нажмите любую клавишу, чтобы закрыть это окно.");
            Console.ReadKey();
        }
    }
}
