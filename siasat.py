from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import multiprocessing as mp

nim = "<nim>"
password = "<password siasat>"

# Masukan kode matkul sesuai matkul pilihan
# kodeMatkul = [["<Kode Matkul>", "<Kode kelas Matkul>"]]

# Contoh
kodeMatkul = [["TC614", "TC614A"], ["TC635", "TC635B"]]

class WarSiasat():
    def setup_selenium(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=options)

        self.browser.get("https://siasat.uksw.edu/default.aspx")       
    
    def stop_method(self):
       self.driver.quit()
    
    def login(self):
        inputNim = self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_TextBox1")
        inputPassword = self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_TextBox2")
        buttonLogin = self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_Button2")
        
        inputNim.send_keys(nim)
        inputPassword.send_keys(password)
        buttonLogin.click()
    
    def registrasi_matkul(self, matkul):
        timeout_secs = 5 
        btnMatkul = WebDriverWait(self.browser, timeout_secs).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@value='" + matkul[0] + "']")))
       
        btnMatkul.click()
        
        btnRegisMatkul = WebDriverWait(self.browser, timeout_secs).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@value='" + matkul[1] + "']")))
        
        btnRegisMatkul.click() 
          
    def close_popup(self):
        timeout_secs = 5
        isPopupActive = WebDriverWait(self.browser, timeout_secs).until(expected_conditions.text_to_be_present_in_element_attribute((By.XPATH, "//div[@id='myModal']"), "style", "display: block;"))
        
        if(isPopupActive):
            btnClose = self.browser.find_element(By.XPATH, "//div[@id='close']")
            btnClose.click()
            
            return True
        else: return True
        
    def main(self, matkul):
        timeout_secs = 5  
        
        self.setup_selenium()
        isPopupClose = self.close_popup()
        if(isPopupClose):
            self.login()
                
        isBtnRegistrasiTrue = WebDriverWait(self.browser, timeout_secs).until(expected_conditions.text_to_be_present_in_element_value((By.ID, "ctl00_ContentPlaceHolder1_Button2"), "REGISTRASI MATAKULIAH"))        
        
        if(isBtnRegistrasiTrue):
            btnRegistrasi = self.browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_Button2")
            btnRegistrasi.click()
            
            self.registrasi_matkul(matkul)

if __name__ == '__main__':
    ws = WarSiasat()

    for kode in kodeMatkul:
        mp.Process(target=ws.main, args=(kode,)).start()
        
        # Multithread, kita spam siasat proses akan dikerjakan secara bersamaan
        for i in range(0,3):
            mp.Process(target=ws.main, args=(kode,)).start()