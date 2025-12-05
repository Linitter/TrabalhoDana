from flask import Flask, jsonify, request, send_from_directory
import os
import sys

# Importar funções de busca
from search_utils import (
    search_sequential,
    search_indexed,
    search_hashmap,
    get_catalog
)

app = Flask(__name__, static_folder='static')

# Configurações
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETEND_X_REQUESTED_WITH'] = True


@app.route('/')
def index():
    """Rota principal"""
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir arquivos estáticos"""
    return send_from_directory('static', filename)


@app.route('/api/search/sequential')
def api_search_sequential():
    """
    GET /api/search/sequential?q=toyota
    Busca sequencial (linear)
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Parâmetro q é obrigatório'}), 400
            
        results = search_sequential(query)
        
        return jsonify({
            'method': 'sequential',
            'query': query,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        print(f"Erro na busca sequencial: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/indexed')
def api_search_indexed():
    """
    GET /api/search/indexed?q=toyota
    Busca indexada
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Parâmetro q é obrigatório'}), 400
            
        results = search_indexed(query)
        
        return jsonify({
            'method': 'indexed',
            'query': query,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        print(f"Erro na busca indexada: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/hash')
def api_search_hash():
    """
    GET /api/search/hash?q=toyota
    Busca usando HashMap
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Parâmetro q é obrigatório'}), 400
            
        results = search_hashmap(query)
        
        return jsonify({
            'method': 'hash',
            'query': query,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        print(f"Erro na busca hash: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/catalog')
def api_catalog():
    """
    GET /api/catalog?page=1
    Retorna catálogo paginado de carros
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limitar per_page para evitar sobrecarga
        per_page = min(per_page, 100)
        
        catalog_data = get_catalog(page=page, per_page=per_page)
        
        return jsonify(catalog_data)
    
    except Exception as e:
        print(f"Erro ao carregar catálogo: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """Tratamento de erro 404"""
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Tratamento de erro 500"""
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("BUSCA DE CARROS USADOS - Sistema de Busca de Carros Usados")
    print("="*60)
    print(f"\nIniciando servidor na porta {port}...")
    print("\nPressione CTRL+C para encerrar\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)