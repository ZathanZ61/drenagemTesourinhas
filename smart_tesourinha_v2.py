import time
import random

# --- 1. CONFIGURAÇÕES E THRESHOLDS (Limites Críticos) ---

# Níveis críticos de água (em centímetros)
NIVEL_ALERTA_L1 = 5.0    # Aciona bombas e alerta de tráfego
NIVEL_BLOQUEIO_L2 = 15.0 # Bloqueio Autônomo
NIVEL_NORMALIZACAO = 3.0 # Nível seguro para desbloqueio (Histerese)

# Taxa de subida (cm/min) considerada PREDITIVA DE RISCO
TAXA_RISCO_PREDITIVO = 2.5 

# --- 2. CLASSE DO SISTEMA CIBER-FÍSICO (CPS) ---

class SmartTesourinhaCPS:
    def __init__(self, nome="Tesourinha Modelo X"):
        """Inicializa o sistema CPS e seu estado."""
        self.nome = nome
        self.nivel_agua_cm = 0.0
        self.taxa_subida_cm_min = 0.0
        self.estado_bombas = False
        self.estado_barreira = "ABERTA"
        
        print(f"[STATUS - {self.nome}] Sistema CPS Inicializado.")
        print("-" * 60)

    def simular_leitura_sensores(self, nivel_anterior):
        """Simula a entrada de dados (Ultrassônico e Câmera de Tráfego)."""
        
        # Simula a variação do nível: pode subir, descer ou estabilizar
        if self.estado_barreira == "FECHADA" and self.estado_bombas == True:
            # Se a barreira está fechada e as bombas ligadas, o nível deve cair.
            aumento_simulado = random.uniform(-1.0, 1.5) 
        else:
            # Simula a chuva: nível sobe mais rapidamente.
            aumento_simulado = random.uniform(0.1, 3.5) 

        novo_nivel = max(0.0, nivel_anterior + aumento_simulado)
        self.nivel_agua_cm = round(novo_nivel, 2)
            
        # Calcula a taxa de subida (para a lógica Preditiva)
        self.taxa_subida_cm_min = round(self.nivel_agua_cm - nivel_anterior, 2)
        
        # Simulação da Visão Computacional: detecta se há tráfego
        trafego_detectado = random.choice([True, False, True, True]) 
        
        print(f"| SENSORES   | Nível: {self.nivel_agua_cm} cm | Taxa: {self.taxa_subida_cm_min} cm/min | Tráfego: {'SIM' if trafego_detectado else 'NÃO'} |")
        
        return trafego_detectado

    def logica_ia_decisao(self):
        """
        Implementa a lógica da IA/ML para decisão de atuação (Core do CPS).
        """
        nivel = self.nivel_agua_cm
        taxa = self.taxa_subida_cm_min
        
        # --- AÇÃO DE SEGURANÇA MÁXIMA (Nível 2: Bloqueio Autônomo) ---
        if nivel >= NIVEL_BLOQUEIO_L2:
            if self.estado_barreira != "FECHADA":
                self.estado_barreira = "FECHADA"
                print(f"[DECISÃO CRÍTICA] BLOQUEIO L2: Nível de {nivel} cm. BARREIRA FECHADA.")
            if not self.estado_bombas:
                self.estado_bombas = True
                print("[DECISÃO CRÍTICA] LIGANDO BOMBAS.")
                
        # --- AÇÃO PREDITIVA E PRÓ-ATIVA (Taxa de Subida Alta ou Alerta L1) ---
        elif (taxa > TAXA_RISCO_PREDITIVO and nivel > NIVEL_ALERTA_L1 * 0.5) and self.estado_barreira != "FECHADA":
            # A IA prevê que o nível crítico será atingido rapidamente
            self.estado_barreira = "FECHADA"
            self.estado_bombas = True
            print(f"[DECISÃO PREDITIVA] TAXA ALTA: Bloqueio antecipado ({taxa} cm/min). BARREIRA FECHADA e BOMBAS LIGADAS.")
        
        # --- AÇÃO DE ALERTA E BOMBEAMENTO (Nível 1) ---
        elif nivel >= NIVEL_ALERTA_L1 and self.estado_barreira == "ABERTA":
            if not self.estado_bombas:
                self.estado_bombas = True
                print("[DECISÃO ALERTA] Nível L1 atingido. LIGANDO BOMBAS e enviando Alerta de Tráfego.")
                
        # --- AÇÃO DE NORMALIZAÇÃO (Margem de Segurança - Histerese) ---
        elif nivel < NIVEL_NORMALIZACAO and self.estado_barreira == "FECHADA":
            # O nível precisa estar bem abaixo do L1 para garantir a segurança antes de desbloquear.
            self.estado_barreira = "ABERTA"
            self.estado_bombas = False
            print(f"[DECISÃO NORMAL] Nível seguro ({nivel} cm). VIA DESBLOQUEADA e BOMBAS DESLIGADAS.")
            
    def acionar_atuadores(self, trafego_detectado):
        """Simula a execução dos comandos nos atuadores (Barreira e Sinalização)."""
        print(f"| ATUADORES  | BARREIRA: {self.estado_barreira} | BOMBAS: {'LIGADAS' if self.estado_bombas else 'DESLIGADAS'} | SINALIZAÇÃO: {'RISCO ALAGAMENTO' if self.estado_barreira == 'FECHADA' else 'NORMAL'} |")
        print("-" * 60)

# --- 3. LOOP PRINCIPAL DE SIMULAÇÃO ---

def simular_operacao_cps(duracao_minutos=15, intervalo_segundos=1):
    """Executa a simulação do loop Ciber-Físico em vários ciclos."""
    tesourinha = SmartTesourinhaCPS("Tesourinha do Eixão")
    nivel_anterior = 0.0
    
    # Simula o tempo (t)
    for t in range(duracao_minutos):
        print(f"\n--- CICLO DE OPERAÇÃO (Tempo {t+1} min) ---")
        
        # 1. MUNDO FÍSICO -> CIBER (Leitura)
        trafego = tesourinha.simular_leitura_sensores(nivel_anterior)
        
        # 2. CIBER (IA/ML) -> Decisão
        tesourinha.logica_ia_decisao()
        
        # 3. CIBER -> MUNDO FÍSICO (Atuação)
        tesourinha.acionar_atuadores(trafego)
        
        nivel_anterior = tesourinha.nivel_agua_cm
        time.sleep(intervalo_segundos) 

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Simula 12 ciclos de 1 minuto (na vida real)
    simular_operacao_cps(duracao_minutos=12, intervalo_segundos=0.5)
