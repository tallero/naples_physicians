#!/usr/bin/env python3

#    Naples Physicians
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from bs4 import BeautifulSoup
from requests import get
import pickle

def save(variable, path):
    """Save variable on given path using Pickle
    
    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        pickle.dump(variable, f)
    f.close()

def load(path):
    """Load variable from Pickle file
    
    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle.load(f)
    f.close()
    return variable

class Physician:
    """Access data from ordinemedicinapoli.it"""
    pattern = "http://www.ordinemedicinapoli.it/scheda_medico.php?id="    

    def get_from_website(self, id):
        """Get physician data from 'ordinemedicinapoli.it' id

        Args:
            id (int): id of the physician on the website
        
        Returns:
            (dict) data on the physician
        """
        page = get(self.pattern + str(id)).content
        soup = BeautifulSoup(page, 'html.parser')
        tds = soup.findAll("td")
        persona = []
        for el in tds:
            if el.attrs == {}:
               persona.append(el.string)
        medico = {"Name":persona[0],
                  "Surname":persona[1],
                  "Birth date":persona[2],
                  "Birth place":persona[3],
                  "Albo":persona[4], 
                  "Registration code":persona[5], 
                  "Degree":persona[6], 
                  "Abilitation Year":persona[7]}
        return medico

    def save_all_to_disk(self):
        """Save on disk all physicians from 'ordinemedicinapoli.it'"""
        physicians = []
        for i in range(1,25149):
            if i % 1000 == 0:
                print(i)
            physicians.append(self.get_from_website(i))

        save(physicians, 'naples_physicians.pkl')

if __name__ == "__main__":
    Physician().save_all_to_disk()
