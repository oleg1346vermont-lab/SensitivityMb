import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. Расчётные функции
# ============================================================

def compute_L(L_path, L_personnel, L_infra):
    return L_path * L_personnel * L_infra

def compute_R(R_tech, R_nat, R_human, R_econ):
    return R_tech + R_nat + R_human + R_econ + 1.0

def compute_Pr(Lc, velocity, S, t_work):
    if t_work == 0:
        return 0.0
    return (Lc * velocity * S * 24) / t_work

def compute_fuel_cost(velocity, t_work, V_fuel_l_per_100km, fuel_price):
    km_per_day = velocity * t_work
    km_per_year = km_per_day * 365
    liters_per_km = V_fuel_l_per_100km / 100.0
    return liters_per_km * km_per_year * fuel_price

def compute_crew_cost(crew_count, crew_monthly_salary):
    return crew_count * crew_monthly_salary * 12

def compute_infrastructure_cost(node_cost, road_cost_per_km, S):
    return node_cost + road_cost_per_km * S

def compute_revenue(velocity, t_work, S, Lc, price_per_ton_km, tax_rate):
    trips_per_year = (velocity * t_work * 365) / S if S > 0 else 0
    tons_per_year = Lc * trips_per_year
    gross = tons_per_year * price_per_ton_km
    return gross * (1 - tax_rate)

def compute_investment(vehicle_fleet_cost, infra_cost, E, fuel_cost, crew_cost):
    return (vehicle_fleet_cost + infra_cost) * E + (fuel_cost + crew_cost)

def compute_Mb(Pr, Re, I, L, R):
    denominator = L * R * I
    if denominator == 0:
        return 0.0
    return (Pr * Re) / denominator

def calculate_Mb_for_params(params):
    L = compute_L(params['L_path'], params['L_personnel'], params['L_infra'])
    R = compute_R(params['R_tech'], params['R_nat'], params['R_human'], params['R_econ'])
    Pr = compute_Pr(params['Lc'], params['velocity'], params['S'], params['t_work'])
    
    if params['special'] is not None:
        m = params['special']['m']
        wagon_cost = params['special']['wagon_cost']
        effective_Lc = params['Lc'] * m
        fleet_cost = params['n_vehicles'] * params['vehicle_cost'] + m * wagon_cost
    else:
        effective_Lc = params['Lc']
        fleet_cost = params['n_vehicles'] * params['vehicle_cost']
    
    infra_cost = compute_infrastructure_cost(params['node_cost'], params['road_cost_per_km'], params['S'])
    fuel_cost = compute_fuel_cost(params['velocity'], params['t_work'], params['V_fuel'], params['fuel_price'])
    crew_cost = compute_crew_cost(params['crew_count'], params['crew_salary'])
    
    Re = compute_revenue(params['velocity'], params['t_work'], params['S'],
                         effective_Lc, params['price_per_ton_km'], params['tax_rate'])
    
    I = compute_investment(fleet_cost, infra_cost, params['E'],
                           fuel_cost, crew_cost)
    
    Mb = compute_Mb(Pr, Re, I, L, R)
    return Mb

# ============================================================
# 2. Базовые параметры
# ============================================================

base_params = {
    'Автомобили': {
        'L_path': 2, 'L_personnel': 1, 'L_infra': 2,
        'R_tech': 0.10, 'R_nat': 0.05, 'R_human': 0.30, 'R_econ': 0.10,
        'Lc': 28.0, 'velocity': 30.0, 'S': 380.0, 't_work': 8.0,
        'V_fuel': 40.0, 'fuel_price': 85.0,
        'crew_count': 1, 'crew_salary': 200000,
        'node_cost': 200_000_000, 'road_cost_per_km': 37000000, 
        'price_per_ton_km': 49.0, 'tax_rate': 0.2,
        'n_vehicles': 1, 'vehicle_cost': 9_000_000,
        'E': 0.125,
        'special': None
    },
    'Речной': {
        'L_path': 3, 'L_personnel': 2, 'L_infra': 2,
        'R_tech': 0.10, 'R_nat': 0.50, 'R_human': 0.03, 'R_econ': 0.05,
        'Lc': 500.0, 'velocity': 7.5, 'S': 772.0, 't_work': 8.0,
        'V_fuel': 167.0, 'fuel_price': 85.0,
        'crew_count': 6, 'crew_salary': 200000,
        'node_cost': 300_000_000, 'road_cost_per_km': 0,
        'price_per_ton_km': 3.0, 'tax_rate': 0.2,
        'n_vehicles': 1, 'vehicle_cost': 100_000_000,
        'E': 0.05,
        'special': {'m': 2, 'wagon_cost': 80_000_000} 
    },
    'Железная дорога': {
        'L_path': 3, 'L_personnel': 2, 'L_infra': 2,
        'R_tech': 0.10, 'R_nat': 0.05, 'R_human': 0.30, 'R_econ': 0.05,
        'Lc': 40.0, 'velocity': 26.66666, 'S': 380.0, 't_work': 8.0,
        'V_fuel': 300.0, 'fuel_price': 40.0,
        'crew_count': 2, 'crew_salary': 150000,
        'node_cost': 200_000_000, 'road_cost_per_km': 67000000, 
        'price_per_ton_km': 11.0, 'tax_rate': 0.2,
        'n_vehicles': 1, 'vehicle_cost': 6_000_000,
        'E': 0.1,
        'special': {'m': 10, 'wagon_cost': 3_000_000}
    },
    'Авиация': {
        'L_path': 1, 'L_personnel': 3, 'L_infra': 3,
        'R_tech': 0.20, 'R_nat': 0.20, 'R_human': 0.10, 'R_econ': 0.20,
        'Lc': 60.0, 'velocity': 126.5, 'S': 259.0, 't_work': 6.0,
        'V_fuel': 130.0, 'fuel_price': 48.0,
        'crew_count': 4, 'crew_salary': 350000,
        'node_cost': 2_100_000_000, 'road_cost_per_km': 0,
        'price_per_ton_km': 150.0, 'tax_rate': 0.2,
        'n_vehicles': 1, 'vehicle_cost': 5_000_000_000,
        'E': 0.05,
        'special': None
    },
    'Дирижабли': {
        'L_path': 1, 'L_personnel': 3, 'L_infra': 3,
        'R_tech': 0.20, 'R_nat': 0.30, 'R_human': 0.10, 'R_econ': 0.20,
        'Lc': 100.0, 'velocity': 65.0, 'S': 259.0, 't_work': 8.0,
        'V_fuel': 80.0, 'fuel_price': 48.0,
        'crew_count': 4, 'crew_salary': 350000,
        'node_cost': 2_100_000_000, 'road_cost_per_km': 0,
        'price_per_ton_km': 150.0, 'tax_rate': 0.2,
        'n_vehicles': 1, 'vehicle_cost': 5_000_000_000,
        'E': 0.05,
        'special': None
    }
}

# ============================================================
# 3. Функция для анализа одного параметра по всем видам
# ============================================================

def analyze_parameter_across_types(parameter_name, param_range_percent=0.2, n_steps=21):
    """
    Анализирует влияние parameter_name на M_b для всех видов транспорта.
    Возвращает словарь с результатами.
    """
    results = {}
    
    for transport_name, params in base_params.items():
        # Проверяем, есть ли параметр в основной части или в special
        if parameter_name in params:
            base_val = params[parameter_name]
            is_special = False
        elif params['special'] is not None and parameter_name in params['special']:
            base_val = params['special'][parameter_name]
            is_special = True
        else:
            # Параметр отсутствует у этого вида транспорта
            continue
        
        delta_frac = np.linspace(-param_range_percent, param_range_percent, n_steps)
        values = base_val * (1 + delta_frac)
        Mb_vals = []
        
        for val in values:
            p_copy = {k: v for k, v in params.items()}
            if not is_special:
                p_copy[parameter_name] = val
            else:
                if p_copy['special'] is not None:
                    p_copy['special'] = params['special'].copy()
                    p_copy['special'][parameter_name] = val
            Mb_vals.append(calculate_Mb_for_params(p_copy))
        
        # Вычисляем эластичность в базовой точке
        base_Mb = calculate_Mb_for_params(params)
        if base_Mb != 0:
            # Производная через центральную разность
            eps = (Mb_vals[-1] - Mb_vals[0]) / (values[-1] - values[0]) * (base_val / base_Mb)
        else:
            eps = 0
        
        results[transport_name] = {
            'values': values,
            'Mb': Mb_vals,
            'elasticity': eps,
            'base_val': base_val,
            'base_Mb': base_Mb
        }
    
    return results

# ============================================================
# 4. Генерация отчётов по каждому параметру
# ============================================================

def create_parameter_report(parameter_name, results, output_dir="отчёты_по_параметрам"):
    """Создаёт HTML-отчёт для одного параметра"""
    
    if not results:
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Подготовка данных для таблицы
    transport_names = list(results.keys())
    n_steps = len(results[transport_names[0]]['values'])
    
    # Создаём DataFrame для таблицы
    table_data = {'Изменение (%)': []}
    
    # Заполняем процентные изменения
    for i in range(n_steps):
        first_transport = transport_names[0]
        pct_change = ((results[first_transport]['values'][i] / results[first_transport]['base_val']) - 1) * 100
        table_data['Изменение (%)'].append(f"{pct_change:.1f}%")
    
    # Добавляем значения M_b для каждого вида транспорта
    for tname in transport_names:
        table_data[tname] = [f"{mb:.4e}" for mb in results[tname]['Mb']]
    
    df = pd.DataFrame(table_data)
    
    # Рисуем график
    plt.figure(figsize=(12, 7))
    for tname in transport_names:
        values_pct = ((results[tname]['values'] / results[tname]['base_val']) - 1) * 100
        plt.plot(values_pct, results[tname]['Mb'], marker='o', markersize=3, 
                 linewidth=1.5, label=f"{tname} (эласт.={results[tname]['elasticity']:.4f})")
    
    plt.xlabel('Изменение параметра (%)', fontsize=12)
    plt.ylabel('M_b', fontsize=12)
    plt.title(f'Влияние параметра "{parameter_name}" на M_b для разных видов транспорта', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    
    # Сохраняем график
    plot_path = os.path.join(output_dir, f"{parameter_name}_plot.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # Ранжирование по эластичности
    elasticities = [(tname, results[tname]['elasticity']) for tname in transport_names]
    elasticities.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Создаём HTML-отчёт
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Анализ чувствительности: {parameter_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #2c3e50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .plot {{ text-align: center; margin: 30px 0; }}
            img {{ max-width: 100%; height: auto; border: 1px solid #ccc; }}
            .elasticity-list {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .note {{ color: #7f8c8d; font-size: 0.9em; margin-top: 20px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
            .back-link {{ display: inline-block; margin-bottom: 20px; color: #3498db; text-decoration: none; }}
            .back-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="index.html" class="back-link">← Назад к списку параметров</a>
            <h1>📊 Анализ чувствительности: параметр <em>"{parameter_name}"</em></h1>
            
            <div class="elasticity-list">
                <h2>📈 Ранжирование по чувствительности (эластичность)</h2>
                <p><strong>Эластичность</strong> = (% изменение M_b) / (% изменение параметра)</p>
                <ol>
    """
    
    for tname, eps in elasticities:
        direction = "положительная" if eps > 0 else "отрицательная"
        sensitivity = "высокая" if abs(eps) > 0.5 else "средняя" if abs(eps) > 0.1 else "низкая"
        html_content += f"<li><strong>{tname}</strong>: {eps:.4f} ({direction} зависимость, {sensitivity} чувствительность)</li>\n"
    
    html_content += f"""
                </ol>
            </div>
            
            <div class="plot">
                <h2>📉 График зависимости M_b от {parameter_name}</h2>
                <img src="{parameter_name}_plot.png" alt="График чувствительности">
            </div>
            
            <h2>📋 Таблица значений M_b</h2>
            {df.to_html(index=False)}
            
            <div class="note">
                <h3>📝 Примечания</h3>
                <p><strong>M_b</strong> — интегральный показатель эффективности транспортной системы. Чем выше значение, тем лучше.</p>
                <p><strong>Базовые значения параметров:</strong></p>
                <ul>
    """
    
    for tname in transport_names:
        html_content += f"<li><strong>{tname}</strong>: {parameter_name} = {results[tname]['base_val']:.4g}, M_b = {results[tname]['base_Mb']:.4e}</li>\n"
    
    html_content += """
                </ul>
                <p><strong>Интерпретация эластичности:</strong><br>
                • |эластичность| > 0.5 — параметр сильно влияет на эффективность<br>
                • 0.1 < |эластичность| < 0.5 — умеренное влияние<br>
                • |эластичность| < 0.1 — слабое влияние</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Сохраняем HTML
    html_path = os.path.join(output_dir, f"{parameter_name}_отчёт.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Создан отчёт: {html_path}")
    return html_path

# ============================================================
# 5. Основная функция генерации всех отчётов
# ============================================================

def generate_all_reports():
    """Генерирует отдельные отчёты для каждого параметра"""
    
    # Список параметров для анализа
    parameters_to_analyze = [
        'Lc', 'velocity', 'S', 't_work', 'V_fuel', 'fuel_price',
        'crew_salary', 'node_cost', 'price_per_ton_km', 'tax_rate', 
        'vehicle_cost', 'E',
        'R_tech', 'R_nat', 'R_human', 'R_econ',
        'L_path', 'L_personnel', 'L_infra',
        'm', 'wagon_cost'
    ]
    
    print("=" * 60)
    print("Генерация отчётов по параметрам")
    print("=" * 60)
    
    generated_reports = []
    
    for param in parameters_to_analyze:
        print(f"\nАнализируем параметр: {param}...")
        results = analyze_parameter_across_types(param, param_range_percent=0.2, n_steps=21)
        if results:
            report_path = create_parameter_report(param, results)
            if report_path:
                generated_reports.append(report_path)
        else:
            print(f"   ⚠️ Параметр {param} не найден ни у одного вида транспорта")
    
    # Создаём главный индексный файл
    if generated_reports:
        create_index_page(generated_reports, output_dir="отчёты_по_параметрам")
    
    print("\n" + "=" * 60)
    print(f"✅ Все отчёты созданы! Найдено: {len(generated_reports)} параметров")
    print(f"📁 Отчёты сохранены в папке: отчёты_по_параметрам/")
    print("📄 Откройте index.html для навигации по всем отчётам")
    print("=" * 60)

def create_index_page(report_paths, output_dir="отчёты_по_параметрам"):
    """Создаёт главную страницу со ссылками на все отчёты"""
    
    # Извлекаем имена параметров из путей файлов
    param_names = []
    for path in report_paths:
        name = os.path.basename(path).replace('_отчёт.html', '')
        param_names.append(name)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Анализ чувствительности транспортных систем</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            h1 { color: #2c3e50; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .report-list { list-style: none; padding: 0; }
            .report-list li { margin: 10px 0; padding: 10px; background: #ecf0f1; border-radius: 5px; transition: 0.3s; }
            .report-list li:hover { background: #bdc3c7; transform: translateX(5px); }
            .report-list a { text-decoration: none; color: #2c3e50; font-weight: bold; display: block; }
            .param-name { font-size: 1.1em; font-family: monospace; }
            .param-desc { font-size: 0.8em; color: #7f8c8d; margin-left: 10px; }
            .footer { margin-top: 30px; text-align: center; color: #7f8c8d; font-size: 0.8em; }
            .summary { background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚛 Анализ чувствительности транспортных систем</h1>
            <div class="summary">
                <p><strong>📊 Всего проанализировано параметров: """ + str(len(param_names)) + """</strong></p>
                <p>Метод: one-at-a-time (изменение каждого параметра на ±20%)</p>
                <p>Для каждого параметра построен график зависимости M_b и рассчитана эластичность</p>
            </div>
            <h2>📑 Отчёты по каждому параметру</h2>
            <ul class="report-list">
    """
    
    for param_name in param_names:
        html_content += f"""
                <li>
                    <a href="{param_name}_отчёт.html">
                        <span class="param-name">📊 {param_name}</span>
                        <span class="param-desc">— анализ влияния на M_b</span>
                    </a>
                </li>
        """
    
    html_content += """
            </ul>
            <div class="footer">
                <p>Методика оценки транспортных систем | Анализ чувствительности методом one-at-a-time</p>
                <p>Каждый отчёт содержит: таблицу значений, график зависимости и ранжирование по эластичности</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Создана главная страница: {index_path}")

# ============================================================
# 6. Запуск
# ============================================================

if __name__ == "__main__":
    generate_all_reports()