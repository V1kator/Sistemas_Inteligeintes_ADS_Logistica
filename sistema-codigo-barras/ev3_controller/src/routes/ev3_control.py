from flask import Blueprint, request, jsonify
from flask_cors import CORS
import logging
import socket
import time

# Importar a biblioteca ev3dev (será usado quando conectado ao EV3 real)
EV3_AVAILABLE = False
MOTOR_PORT = None
try:
    from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
    from ev3dev2.sensor import INPUT_1
    from ev3dev2.sensor.lego import TouchSensor
    EV3_AVAILABLE = True
    MOTOR_PORT = OUTPUT_A  # Porta onde o motor do seletor está conectado
except ImportError:
    logging.warning("Biblioteca ev3dev2 não encontrada. Executando em modo simulação.")

ev3_control_bp = Blueprint("ev3_control", __name__)
CORS(ev3_control_bp)  # Permite requisições CORS para este blueprint

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações do motor EV3
MOTOR_SPEED = 50  # Velocidade do motor (ajustável)# Posições do seletor (em graus)
POSITIONS = {
    1: -90,   # Esquerda (Norte/Nordeste)
    2: 90,    # Direita (Sul/Sudeste)
    3: 0      # Centro/Reto (Centro-Oeste)
}

@ev3_control_bp.route('/control_ev3', methods=['POST'])
def control_ev3():
    """
    Endpoint para receber comandos de controle do EV3 baseados no ponto de entrega.
    
    Espera um JSON com:
    {
        "delivery_point": 1|2|3
    }
    
    Retorna:
    {
        "success": true|false,
        "message": "Mensagem de status",
        "action": "Ação executada",
        "ev3_connected": true|false
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "Nenhum dado JSON fornecido"
            }), 400
        
        delivery_point = data.get('delivery_point')
        
        if delivery_point not in [1, 2, 3]:
            return jsonify({
                "success": False,
                "message": "Ponto de entrega deve ser 1, 2 ou 3"
            }), 400
        
        # Determinar a ação com base no ponto de entrega
        action = determine_action(delivery_point)
        
        # Executar o comando no EV3
        success, error_msg = execute_ev3_command(delivery_point, action)
        
        if success:
            logger.info(f"Comando EV3 executado com sucesso: {action}")
            return jsonify({
                "success": True,
                "message": f"Comando executado com sucesso",
                "action": action,
                "delivery_point": delivery_point,
                "ev3_connected": EV3_AVAILABLE
            })
        else:
            logger.error(f"Falha ao executar comando EV3: {action} - {error_msg}")
            return jsonify({
                "success": False,
                "message": f"Falha ao executar comando no EV3: {error_msg}",
                "action": action,
                "ev3_connected": EV3_AVAILABLE
            }), 500
            
    except Exception as e:
        logger.error(f"Erro no endpoint control_ev3: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Erro interno do servidor: {str(e)}",
            "ev3_connected": EV3_AVAILABLE
        }), 500

def determine_action(delivery_point):
    """
    Determina a ação do motor com base no ponto de entrega.
    
    Args:
        delivery_point (int): Ponto de entrega (1, 2 ou 3)
    
    Returns:
        str: Descrição da ação a ser executada
    """
    actions = {
        1: "Direcionar para a esquerda (Norte/Nordeste)",
        2: "Direcionar para a direita (Sul/Sudeste)", 
        3: "Manter reto (Centro-Oeste)"
    }
    return actions.get(delivery_point, "Ação desconhecida")

def execute_ev3_command(delivery_point, action):
    """
    Executa o comando no LEGO EV3.
    
    Args:
        delivery_point (int): Ponto de entrega
        action (str): Descrição da ação
    
    Returns:
        tuple: (success: bool, error_message: str)
    """
    try:
        if EV3_AVAILABLE:
            # Código real para controlar o EV3
            logger.info(f"Conectando ao motor EV3 na porta {MOTOR_PORT}")
            
            # Inicializar o motor
            motor = LargeMotor(MOTOR_PORT)
            
            # Verificar se o motor está conectado
            if not motor.connected:
                return False, "Motor não conectado na porta especificada"
            
            # Obter a posição alvo
            target_position = POSITIONS.get(delivery_point, 0)
            
            # Mover o motor para a posição
            logger.info(f"Movendo motor para posição {target_position} graus")
            motor.on_to_position(MOTOR_SPEED, target_position)
            
            # Aguardar o movimento completar
            motor.wait_until_not_moving()
            
            logger.info(f"Motor posicionado com sucesso: {action}")
            return True, ""
            
        else:
            # Modo simulação quando o EV3 não está disponível
            logger.info(f"[SIMULAÇÃO] Executando no EV3: Ponto {delivery_point} - {action}")
            logger.info(f"[SIMULAÇÃO] Movendo motor para posição {POSITIONS.get(delivery_point, 0)} graus")
            
            # Simular tempo de movimento
            time.sleep(1)
            
            return True, ""
            
    except Exception as e:
        error_msg = f"Erro ao executar comando EV3: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def check_ev3_connection():
    """
    Verifica se o EV3 está conectado e acessível.
    
    Returns:
        dict: Status da conexão
    """
    if not EV3_AVAILABLE:
        return {
            "connected": False,
            "message": "Biblioteca ev3dev2 não disponível",
            "mode": "simulation"
        }
    
    try:
        # Tentar inicializar o motor para verificar conexão
        motor = LargeMotor(MOTOR_PORT)
        if motor.connected:
            return {
                "connected": True,
                "message": "EV3 conectado e motor disponível",
                "mode": "real",
                "motor_port": str(MOTOR_PORT)
            }
        else:
            return {
                "connected": False,
                "message": f"Motor não encontrado na porta {MOTOR_PORT}",
                "mode": "simulation"
            }
    except Exception as e:
        return {
            "connected": False,
            "message": f"Erro ao conectar com EV3: {str(e)}",
            "mode": "simulation"
        }

@ev3_control_bp.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint para verificar o status do servidor e da conexão com o EV3.
    """
    ev3_status = check_ev3_connection()
    
    return jsonify({
        "server_status": "online",
        "ev3_status": ev3_status,
        "library_available": EV3_AVAILABLE,
        "supported_delivery_points": [1, 2, 3],
        "motor_positions": POSITIONS,
        "message": "Servidor EV3 Controller funcionando"
    })

@ev3_control_bp.route('/test_motor', methods=['POST'])
def test_motor():
    """
    Endpoint para testar o motor do EV3 sem depender do ponto de entrega.
    Útil para calibração e testes.
    """
    try:
        data = request.get_json()
        position = data.get('position', 0) if data else 0
        
        if EV3_AVAILABLE:
            motor = LargeMotor(MOTOR_PORT)
            if motor.connected:
                motor.on_to_position(MOTOR_SPEED, position)
                motor.wait_until_not_moving()
                return jsonify({
                    "success": True,
                    "message": f"Motor movido para posição {position} graus",
                    "position": position
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "Motor não conectado"
                }), 500
        else:
            logger.info(f"[SIMULAÇÃO] Teste de motor: posição {position} graus")
            return jsonify({
                "success": True,
                "message": f"[SIMULAÇÃO] Motor movido para posição {position} graus",
                "position": position,
                "mode": "simulation"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro no teste do motor: {str(e)}"
        }), 500

