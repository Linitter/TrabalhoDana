/**
 * main.js
 * Lógica do front-end para as buscas
 */

/**
 * Realiza a busca na API
 */
async function performSearch(method, query) {
    const resultsContainer = document.getElementById('results-container');
    const resultsInfo = document.getElementById('results-info');
    const searchBtn = document.getElementById('search-btn');
    
    if (!resultsContainer || !searchBtn) {
        console.error('Elementos não encontrados');
        return;
    }
    
    // Mostrar loading
    resultsContainer.innerHTML = '<div class="loading">🔍 Buscando...</div>';
    if (resultsInfo) {
        resultsInfo.classList.remove('show');
    }
    searchBtn.disabled = true;
    
    // Iniciar cronômetro
    const startTime = performance.now();
    
    try {
        // Fazer requisição
        const response = await fetch(`/api/search/${method}?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Erro na busca');
        }
        
        const data = await response.json();
        const endTime = performance.now();
        const duration = (endTime - startTime).toFixed(2);
        
        // Mostrar informações
        if (resultsInfo) {
            resultsInfo.innerHTML = `
                <span class="stat">✅ Encontrados: <strong>${data.count}</strong> resultados</span>
                <span class="stat">⏱️ Tempo: <strong>${duration}ms</strong></span>
                <span class="stat">📊 Algoritmo: <strong>${getAlgorithmName(method)}</strong></span>
            `;
            resultsInfo.classList.add('show');
        }
        
        // Renderizar resultados
        renderResults(resultsContainer, data.results);
        
    } catch (error) {
        resultsContainer.innerHTML = `
            <div class="error">
                ❌ Erro ao realizar busca: ${error.message}
            </div>
        `;
        if (resultsInfo) {
            resultsInfo.classList.remove('show');
        }
    } finally {
        searchBtn.disabled = false;
    }
}

/**
 * Renderiza os resultados na tela
 */
function renderResults(container, results) {
    if (!results || results.length === 0) {
        container.innerHTML = `
            <div class="empty">
                🔍 Nenhum resultado encontrado.<br>
                Tente outro termo de busca.
            </div>
        `;
        return;
    }
    
    const grid = document.createElement('div');
    grid.className = 'results-grid';
    
    results.forEach(car => {
        const price = formatPrice(car.price);
        
        const card = document.createElement('div');
        card.className = 'car-card';
        card.innerHTML = `
            <div class="car-brand">${escapeHtml(car.brand)}</div>
            <div class="car-model">${escapeHtml(car.model)}</div>
            <div class="car-details">
                <span class="car-year">📅 ${car.year}</span>
                <span class="car-price">${price}</span>
            </div>
        `;
        
        grid.appendChild(card);
    });
    
    container.innerHTML = '';
    container.appendChild(grid);
}

/**
 * Formata o preço
 */
function formatPrice(price) {
    if (!price || price === 0) {
        return 'N/A';
    }
    
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(price);
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Retorna o nome do algoritmo
 */
function getAlgorithmName(method) {
    const names = {
        'sequential': 'Busca Sequencial',
        'indexed': 'Busca Indexada',
        'hash': 'Busca HashMap'
    };
    return names[method] || method;
}

/**
 * Inicialização
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚗 USED CARS SEARCH inicializado');
    console.log('✅ Sistema pronto para buscas');
});
