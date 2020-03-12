from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import time
import datetime
import pytest
import json
import sys

debug = True
if not debug:
	driver = webdriver.Chrome()
	driver.get("https:/1olimp.com")
	print('Если залогинился нажми ентер')
	input()
	tvgames = driver.find_element_by_xpath("/html/body/header/div[2]/div[2]/div/ul/li[4]/a")
	tvgames.click()
	print('Заходим на Бетгеймс')
	time.sleep(5)
	driver.switch_to.frame('betgames_iframe_1')
	print('Переключились на фрейм')
	time.sleep(3)
	koleso = driver.find_element_by_xpath("/html/body/div/div/nav[2]/div/div/div[2]/div[4]/div[1]/span")
	koleso.click()

log = 'log.txt'

def f(a, price):
	if a == '0':
		return
	print('ставим на', a)
	if not debug:
		d = driver.find_element_by_xpath("//div[@class='odd-item-info']")
		d.click()
		for _ in range(10):
			try:
				time.sleep(0.1)
				d = driver.find_element_by_xpath("//span[@data-qa='button-game-item-select-" + str(a) + "']")
				d.click()
				break
			except:
				continue
		for _ in range(10):
			try:
				time.sleep(0.1)
				d = driver.find_element_by_xpath("//button[@class='odd-item-dropdown-confirm']")
				d.click()
				break
			except:
				continue
		for _ in range(10):
			try:
				time.sleep(0.1)
				d = driver.find_element_by_xpath("//input[@data-qa='input-bet-slip-amount']")
				d.click()
				d.sendKeys(Keys.chord(Keys.CONTROL,"a", Keys.DELETE));
				break
			except:
				continue
	#	d = driver.find_element_by_xpath('/html/body/div/div/main/section[2]/div[2]/div[1]/footer/div[1]/div[2]/input')
		price0 = str(int(price))
		print('ставим', price0, 'тг')
		d.clear()
		for symbol in price0:
			d.send_keys(symbol)
			time.sleep(0.05)
		while True:
			try:
				time.sleep(0.1)
				d = driver.find_element_by_xpath("//button[@data-qa='button-place-bet']")
				break
			except:
				continue
		d.click()

mass = [1, 1, 2, 2, 3, 2, 4, 5, 5, 6, 5, 9, 9, 10, 11, 9, 1, 6, 7, 8]
price = 100
n = 4
coeff = 1.1
if not debug:
	mass.clear()

def find_pair(x, i):
	j = i + 1
	while j < len(x):
		if x[j] == x[j - 1]:
			return j
		j += 1
	return -1

def exists(x, i, val, n):
	j = i
	while j < len(x) and j < i + n:
		if x[j] == val:
			return j
		j += 1
	if len(x) - i >= n:
		return -1 # definetely wont exist
	return -2 # need to wait

x = []
i = 0
a = -1
while True:
	if not debug:
		timet = driver.find_element_by_xpath("/html/body/div/div/nav[2]/div/div/div[2]/div[4]/div[2]/span")
		while True:
			try:
				time.sleep(0.2)
				timet = driver.find_element_by_xpath("/html/body/div/div/nav[2]/div/div/div[2]/div[4]/div[2]/span")
				print(timet.text)
				if timet.text == '00:45':
					a1 = driver.find_element_by_xpath("/html/body/div/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div[2]/span/span/span")
					a = a1.text
					time.sleep(1)
					break
			except KeyboardInterrupt:
				print('пока')
				sys.exit(0)
			except:
				print('STACK TRACE:', e.stacktrace())
				print('no such element trying again, все ок')
		print('время пришло 00:45:')
		#	mass.append(a1.text)
#		print(mass)
		#a = int(random.random() * 5)
	else:
		if i >= len(mass):
			break
		a = mass[i]
		i += 1
	x.append(a)
	print(a, x)
	# f(a, price)
	# price *= coeff
	bets = [-1] * len(x)
	#print(a, x)
	j = find_pair(x, 0)
	if j < 0:
		x = x[-1:]
		continue
	if exists(x, j + 1, x[j], n) >= 0:
		x = x[-1:]
		continue
#	print('pair 1:', x[j])
	k = find_pair(x, j + 1)
	if k < 0:
		continue
	d = exists(x, k + 1, x[k], n)
	if d == -1:
		x = x[k - 1:]
		continue
	elif d == -2:
		continue
#	print('pair 2:', x[k])
	pair = 0
	e = d
	while pair < 3 and e >= 0:
		e = find_pair(x, e + 1)
		if e < 0:
			break
		d = exists(x, e + 1, x[e], n)
		g = e
		while g < e + n and g < len(x) and (g <= d and d >= 0 or d < 0):
			bets[g] = x[e]
			g += 1
		e = g - 1
		if d >= 0:
			pair += 1
#	print(x)
#	print('bets', bets)
	if int(bets[-1]) >= 0:
		f(bets[-1], price)
		price *= 1.1
#	print('pair', pair)
	if pair >= 3:
		x.clear()
	if not debug:
		time.sleep(1)
		timet = driver.find_element_by_xpath("/html/body/div/div/nav[2]/div/div/div[2]/div[4]/div[2]/span")