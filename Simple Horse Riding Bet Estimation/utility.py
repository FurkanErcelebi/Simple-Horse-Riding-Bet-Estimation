import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_race(date):
    
    url = 'https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami'
    path_to_driver = 'chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(path_to_driver, chrome_options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='QueryParameter_Tarih']").clear()
    driver.find_element_by_xpath("//*[@id='QueryParameter_Tarih']").send_keys(date)
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='İstanbul']").click()
    time.sleep(5)
    div_tables = driver.find_elements_by_xpath("//*[@id='İstanbul']/div[4]/*")
    
    data_frames = []
    for table_html in div_tables:
        html = table_html.get_attribute('innerHTML')
        df_html = pd.read_html(html)
        df_html = pd.DataFrame(df_html[0])
        data_frames.append(df_html)
    

    return data_frames

        
def calculate_order(value):
    
    str_order = str(value)
    str_len = len(str_order)
    step = 0
    avg = 0
    jump = 0
    if str_order != 'nan':
        for num in range(str_len):
            if str_order[num] != '-':
                if jump == 0:
                    avg = avg + int(str_order[num])
                    step = step + 1
                else:
                    jump = 0
            else:
                jump = 1
    
        if step != 0:
            avg = avg / step
        
    return avg
        
def get_bet_result(data_frame):
    horses = data_frame['At İsmi']
    bet_result = []
    for horse in horses:
        str_len = len(horse)
        for i in range(str_len):
            if horse[i] == '(':
                a = i + 1
                while(horse[i] != ')'):
                    i += 1
                if horse[a:i].isnumeric():
                    value = int(horse[a:i])
                    bet_result.append(value)
                    
    return bet_result

def get_estimates(x,y,estimates,real_results,limit):

    print('Estimated bet from starting from {}. contestant in {}. competition  with order limit {}'.format(x,y,limit))
    length = len(estimates)
    if length == 0:
        print('No estimates found')
    else:
        for estimate in estimates:
            x = estimate[0]
            y = estimate[1]
            print('In {} run , {} number horse finished  at {}. order'.format(y,x,int(real_results[y][x])))
    

def get_accuracy(max_val,estimate_results, real_results):
    accuracy = 0

    for estimate_result in estimate_results:
        x = estimate_result[0]
        y = estimate_result[1] 
        cost = estimate_result[2]
        accuracy += (real_results[y][x] - 1) *(cost/max_val)
    
    if accuracy > 0:
       accuracy = 1 / accuracy
       
    return accuracy 
    
def get_min_cost(costs):

    i = 0
    min = 20
    min_i = -1
    for cost in costs:
        if cost < min:
            min = cost
            min_i = i
            
        i = i + 1
        
    return min_i

def is_traveled(possible_race_results, current):

    for result in possible_race_results:
        if result[0] == current[0] and result[1] == current[1]:
            return True
                    
    return False


def generate_other_results(bets, current,way,limit):
    
    x_bound = len(bets[0])
    x = current[0]
    y = current[1]
    
    other_options = []
    if way == 'down':
        if (x - 1) > -1 and (x - 1) < x_bound:
            if limit > bets[y - 1][x - 1] and bets[y - 1][x - 1] > 0:
                avg = 0
                for i in range(y - 1, -1, -1):
                    avg = avg + bets[i][x - 1]
                avg = avg / y
                    
                new_one = []
                new_one.append(x - 1)
                new_one.append(y - 1)
                g = current[2] 
                h = bets[y][x - 1] + avg
                new_one.append(g + h)
                other_options.append(new_one)
                
        
        if x > -1 and x < x_bound:
            if limit > bets[y - 1][x] and bets[y - 1][x - 1] > 0:
                avg = 0
                for i in range(y-1, -1, -1):
                    avg = avg + bets[i][x]
                avg = avg / y
                    
                new_one = []
                new_one.append(x)
                new_one.append(y - 1)
                g = current[2] 
                h = bets[y][x] + avg
                new_one.append(g + h)
                other_options.append(new_one)
        
        if (x + 1) > -1 and (x + 1) < x_bound:
            if limit > bets[y - 1][x + 1] and bets[y - 1][x - 1] > 0:
                avg = 0
                for i in range(y-1, -1, -1):
                    avg = avg + bets[i][x + 1]
                avg = avg / y
                    
                new_one = []
                new_one.append(x + 1)
                new_one.append(y - 1)
                g = current[2] 
                h = bets[y][x + 1] + avg
                new_one.append(g + h)
                other_options.append(new_one) 
                 
    if way == 'up':
        if (x - 1) > -1 and (x - 1) < x_bound:
            if limit > bets[y + 1][x - 1] and bets[y + 1][x - 1] > 0:
                avg = 0
                for i in range(y + 1):
                    avg = avg + bets[i][x - 1]
                avg = avg / y
                    
                new_one = []
                new_one.append(x - 1)
                new_one.append(y + 1)
                g = current[2] 
                h = bets[y][x - 1] + avg
                new_one.append(g + h)
                other_options.append(new_one)
        
        if x > -1 and x < x_bound:
            if limit > bets[y + 1][x] and bets[y + 1][x - 1] > 0:
                avg = 0
                for i in range(y + 1):
                    avg = avg + bets[i][x]
                avg = avg / y
                    
                new_one = []
                new_one.append(x)
                new_one.append(y + 1)
                g = current[2] 
                h = bets[y][x] + avg
                new_one.append(g + h)
                other_options.append(new_one)
        
        if (x + 1) > -1 and (x + 1) < x_bound:
            if limit > bets[y + 1][x + 1] and bets[y + 1][x - 1] > 0:
                avg = 0
                for i in range(y + 1):
                    avg = avg + bets[i][x + 1]
                avg = avg / y
                    
                new_one = []
                new_one.append(x + 1)
                new_one.append(y + 1)
                g = current[2] 
                h = bets[y][x + 1] + avg
                new_one.append(g + h)
                other_options.append(new_one) 
        
    
    return other_options


def  a_start_search_for_optimization(horse_competition_bets,start_point,way,limit):
    
    # we use these two variables at the time of visualisations
    iterations = 0
    
    competitions = len(horse_competition_bets)
    
    iterations += 1
    
    possible_race_results = []
    stack_list = []
    stack_list.append(start_point)
    
    iterations += 1
    
    while stack_list:
        
        tmp = [info[2] for info in stack_list]
        current_i = get_min_cost(tmp)
        
        current = stack_list[current_i]
        del stack_list[current_i]
        
        iterations += 1
        
        #control whether it reached last competition
        if way == 'up':
            if current[1] == competitions:
                iterations += 1
                return(iterations, possible_race_results)
            
        if way == 'down':
            if current[1] == 0:
                iterations += 1
                return(iterations, possible_race_results)
        
        for other_bets in generate_other_results(horse_competition_bets,current,way,limit):
            if not is_traveled(possible_race_results, other_bets):
                possible_race_results.append(other_bets)
                stack_list.append(other_bets)
                iterations += 1
    
        
    return(iterations, possible_race_results)

def show_results(accuracies,i):
    fig, ax = plt.subplots()
    sns.lineplot(
        data=accuracies,
        dashes=False,
        palette="Set1",
        marker="o",
        alpha=0.5,
        ax=ax,
    )
    ax.set_xlabel("Average Order Limits(3-7)", size=16, labelpad=5)
    ax.set_ylabel("Accuracy", size=13)
    ax.tick_params(bottom=True, labelbottom=False)
    plt.savefig('Horse_riding_bet_estimation_{}.png'.format(i))
    plt.show()


