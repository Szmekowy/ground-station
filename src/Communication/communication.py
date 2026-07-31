import time
import json
import RPi.GPIO as GPIO

# Zakładamy użycie wrappera dostarczonego przez producenta (SBCShop/Waveshare)
# Jeśli biblioteka nazywa się inaczej, należy podmienić import.
# Przyjmujemy abstrakcyjną klasę reprezentującą sterownik SX1262.
from sx126x import sx126x 

class Communication:
    def __init__(self):
        print("Inicjalizacja stacji naziemnej (Raspberry Pi + LoRa SX1262)...")
        # Inicjalizacja modułu z odpowiednią częstotliwością (np. 868 MHz dla Europy)
        self.lora = sx126x(serial_num='/dev/ttyS0', freq=868, addr=0, power=22, rssi=True, air_speed=2400)
        self.lora.begin()
        print("Moduł LoRa gotowy.")

    def send_data(self, payload_dict):
        """
        Wysyła dane do balonu w formacie JSON.
        """
        try:
            # Kompresja słownika do stringa JSON i zamiana na bajty
            data_str = json.dumps(payload_dict)
            data_bytes = data_str.encode('utf-8')
            
            # Wysłanie danych przez moduł
            self.lora.send(data_bytes)
            print(f"[TX] Wysłano: {data_str}")
            return True
        except Exception as e:
            print(f"[TX_ERROR] Błąd podczas wysyłania: {e}")
            return False

    def receive_data(self, timeout=5.0):
        """
        Oczekuje na dane z balonu przez określony czas (timeout).
        Zwraca sparsowany słownik JSON i wartość RSSI (jakość sygnału).
        """
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            packet = self.lora.receive()
            
            if packet:
                rssi = self.lora.get_rssi()
                try:
                    payload_str = packet.decode('utf-8')
                    payload_dict = json.loads(payload_str)
                    print(f"[RX] Odebrano (RSSI: {rssi} dBm): {payload_dict}")
                    return payload_dict, rssi
                except json.JSONDecodeError:
                    print(f"[RX_WARNING] Odebrano uszkodzony lub nie-JSON pakiet: {packet}")
                    return {"raw_data": packet.decode('utf-8', errors='ignore')}, rssi
                    
            time.sleep(0.1) 
            
        return None, None 

    def ping_balloon(self):
        """
        KROK 1: Sprawdzenie połączenia.
        Wysyła PING i czeka na PONG od balonu.
        """
        print("\n--- Sprawdzanie połączenia (PING) ---")
        self.send_data({"c": "PING"})
        
        response, rssi = self.receive_data(timeout=3.0)
        
        if response and response.get("s") == "PONG":
            print(f"[SUCCESS] Połączenie nawiązane! Jakość sygnału: {rssi} dBm")
            return True
        else:
            print("[FAILED] Brak odpowiedzi od balonu. Upewnij się, że antena jest podłączona.")
            return False

    def trigger_cut_rope(self):
        """
        KROK 2: Kontrola - wysłanie krytycznej komendy.
        """
        print("\n!!! WYSYŁANIE KOMENDY ODCIĘCIA LINY !!!")
        self.send_data({"c": "CUT_ROPE"})
        
        # Czekamy na potwierdzenie od balonu, że komenda została wykonana
        response, _ = self.receive_data(timeout=5.0)
        if response and response.get("s") == "ROPE_CUT_CONFIRMED":
            print("Balon potwierdził odcięcie liny!")
        else:
            print("Brak potwierdzenia odcięcia liny. Należy ponowić próbę.")

    def listen_for_telemetry(self):
        """
        KROK 3: Nasłuch danych.
        Główna pętla odbierająca dane i przekazująca je do Backend'u.
        """
        print("\nNasłuchiwanie telemetrii...")
        try:
            while True:
                data, rssi = self.receive_data(timeout=1.0)
                if data:
                    if "t" in data: 
                        self._forward_to_backend(data, rssi)
                    else:
                        print(f"Nierozpoznany pakiet: {data}")
        except KeyboardInterrupt:
            print("Zatrzymano nasłuch.")

    def _forward_to_backend(self, data, rssi):
        """
        Przekazanie danych backendowi
        """
        print(f"-> [BACKEND] Zapisywanie danych: Temp: {data.get('t')}C, Alt: {data.get('alt')}m, RSSI: {rssi}")


# Przykładowe użycie:
if __name__ == "__main__":
    station = Communication()
    
    # 1. Sprawdź połączenie
    if station.ping_balloon():
        # 2. Jeśli połączono, rozpocznij nasłuch telemetrii
        # (W prawdziwym systemie odcięcie liny 'trigger_cut_rope' byłoby wywoływane 
        # asynchronicznie przez backend, np. za pomocą MQTT lub wątku).
        station.listen_for_telemetry()