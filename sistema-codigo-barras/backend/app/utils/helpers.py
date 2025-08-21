"""
Funções auxiliares (helpers) para o Sistema de Códigos de Barras por CEP
"""

import re
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

def format_cep(cep: str) -> str:
    """
    Formata CEP no padrão brasileiro 00000-000
    
    Args:
        cep (str): CEP apenas números
        
    Returns:
        str: CEP formatado
    """
    if not cep:
        return ""
    
    cep_limpo = clean_cep(cep)
    if len(cep_limpo) == 8:
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    return cep

def clean_cep(cep: str) -> str:
    """
    Remove formatação do CEP, mantendo apenas números
    
    Args:
        cep (str): CEP com ou sem formatação
        
    Returns:
        str: CEP apenas números
    """
    if not cep:
        return ""
    return re.sub(r'[^0-9]', '', cep.strip())

def generate_filename(prefix: str = "file", extension: str = "png") -> str:
    """
    Gera nome único para arquivo
    
    Args:
        prefix (str): Prefixo do nome do arquivo
        extension (str): Extensão do arquivo (sem ponto)
        
    Returns:
        str: Nome único do arquivo
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    if not extension.startswith('.'):
        extension = f".{extension}"
    
    return f"{prefix}_{timestamp}_{unique_id}{extension}"

def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em formato legível
    
    Args:
        size_bytes (int): Tamanho em bytes
        
    Returns:
        str: Tamanho formatado (ex: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza nome de arquivo removendo caracteres inválidos
    
    Args:
        filename (str): Nome do arquivo original
        
    Returns:
        str: Nome do arquivo sanitizado
    """
    if not filename:
        return "arquivo"
    
    # Remove caracteres especiais e espaços
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    
    # Limita tamanho
    if len(sanitized) > 100:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:95] + ext
    
    return sanitized or "arquivo"

def format_datetime(dt: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Formata datetime para string
    
    Args:
        dt (datetime): Objeto datetime
        formato (str): Formato de saída
        
    Returns:
        str: Data formatada
    """
    if not dt:
        return ""
    
    try:
        return dt.strftime(formato)
    except:
        return str(dt)

def parse_datetime(dt_str: str, formato: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Converte string para datetime
    
    Args:
        dt_str (str): String da data
        formato (str): Formato de entrada
        
    Returns:
        Optional[datetime]: Objeto datetime ou None
    """
    if not dt_str:
        return None
    
    try:
        return datetime.strptime(dt_str, formato)
    except:
        return None

def create_response(data: Any = None, message: str = "", success: bool = True, 
                   status_code: int = 200, errors: list = None) -> Dict:
    """
    Cria resposta padronizada para API
    
    Args:
        data: Dados da resposta
        message (str): Mensagem da resposta
        success (bool): Indica se foi bem-sucedido
        status_code (int): Código de status HTTP
        errors (list): Lista de erros
        
    Returns:
        Dict: Resposta padronizada
    """
    response = {
        "success": success,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    if errors:
        response["errors"] = errors
    
    return response

def create_error_response(message: str, status_code: int = 400, 
                         errors: list = None, details: str = None) -> Dict:
    """
    Cria resposta de erro padronizada
    
    Args:
        message (str): Mensagem de erro
        status_code (int): Código de status HTTP
        errors (list): Lista de erros específicos
        details (str): Detalhes adicionais do erro
        
    Returns:
        Dict: Resposta de erro padronizada
    """
    response = create_response(
        message=message,
        success=False,
        status_code=status_code,
        errors=errors
    )
    
    if details:
        response["details"] = details
    
    return response

def create_success_response(data: Any = None, message: str = "Operação realizada com sucesso",
                           status_code: int = 200) -> Dict:
    """
    Cria resposta de sucesso padronizada
    
    Args:
        data: Dados da resposta
        message (str): Mensagem de sucesso
        status_code (int): Código de status HTTP
        
    Returns:
        Dict: Resposta de sucesso padronizada
    """
    return create_response(
        data=data,
        message=message,
        success=True,
        status_code=status_code
    )

def paginate_query(query, page: int = 1, per_page: int = 10, max_per_page: int = 100):
    """
    Aplica paginação a uma query SQLAlchemy
    
    Args:
        query: Query SQLAlchemy
        page (int): Número da página
        per_page (int): Itens por página
        max_per_page (int): Máximo de itens por página
        
    Returns:
        Objeto de paginação
    """
    # Valida parâmetros
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def extract_region_from_code(codigo: str) -> int:
    """
    Extrai identificador de região do código de barras
    
    Args:
        codigo (str): Código completo
        
    Returns:
        int: Identificador da região (1, 2 ou 3)
    """
    if not codigo or len(codigo) < 1:
        return 1
    
    try:
        regiao = int(codigo[0])
        return regiao if regiao in [1, 2, 3] else 1
    except (ValueError, IndexError):
        return 1

def validate_image_file(file_path: str) -> bool:
    """
    Valida se o arquivo é uma imagem válida
    
    Args:
        file_path (str): Caminho do arquivo
        
    Returns:
        bool: True se é uma imagem válida
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            img.verify()
        return True
    except:
        return False

def get_file_info(file_path: str) -> Dict:
    """
    Obtém informações de um arquivo
    
    Args:
        file_path (str): Caminho do arquivo
        
    Returns:
        Dict: Informações do arquivo
    """
    if not os.path.exists(file_path):
        return {}
    
    try:
        stat = os.stat(file_path)
        return {
            "nome": os.path.basename(file_path),
            "tamanho": stat.st_size,
            "tamanho_formatado": format_file_size(stat.st_size),
            "data_criacao": datetime.fromtimestamp(stat.st_ctime),
            "data_modificacao": datetime.fromtimestamp(stat.st_mtime),
            "extensao": os.path.splitext(file_path)[1].lower()
        }
    except:
        return {}

def clean_string(text: str, max_length: int = None) -> str:
    """
    Limpa e sanitiza string
    
    Args:
        text (str): Texto a ser limpo
        max_length (int): Tamanho máximo
        
    Returns:
        str: Texto limpo
    """
    if not text:
        return ""
    
    # Remove espaços extras
    cleaned = ' '.join(text.strip().split())
    
    # Limita tamanho se especificado
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length].strip()
    
    return cleaned

