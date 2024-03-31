code = '''/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dhubleur <dhubleur@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/07/12 12:43:14 by dhubleur          #+#    #+#             */
/*   Updated: 2023/07/12 12:43:23 by dhubleur         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print(char c)
{
	write(1, &c, 1);
}

void	ft_putchar(char c)
{
	ft_print(c + 1);
}
'''

function = '''/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dhubleur <dhubleur@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/07/12 12:43:14 by dhubleur          #+#    #+#             */
/*   Updated: 2023/07/12 12:43:23 by dhubleur         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print(char c)
{
	write(1, &c, 1);
}

void	ft_putchar(char c)
{
	ft_print(c);
}
'''

main = '''
/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dhubleur <dhubleur@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/07/12 12:42:17 by dhubleur          #+#    #+#             */
/*   Updated: 2023/07/12 12:42:55 by dhubleur         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_putchar(char c);

int	main()
{
	for (int i = ' '; i <= '~'; i++)
		ft_putchar(i);
	ft_putchar('\\n');
	ft_putchar('\\t');
	ft_putchar('\\n');
}
'''

functions = ['write']

flags = '-Wall -Wextra -Werror'

subject = 'ft_putchar'

client = 42

tries_count = 1

import requests
import json

url = 'http://localhost:3000/'
data = {
	'content': {
		'files': {
			'ft_putchar.c': code
		},
		'function': function,
		'main': main
	},
	'flags': flags,
	'functions': functions,
	'run': {
		'subject': subject,
		'client': client,
		'try': tries_count
	}
}

response = requests.post(url, json=data)

with open('response.txt', 'w') as f:
	f.write(response.json()['trace'])
res = response.json()
res['trace'] = '...'
print(json.dumps(res, indent=4))