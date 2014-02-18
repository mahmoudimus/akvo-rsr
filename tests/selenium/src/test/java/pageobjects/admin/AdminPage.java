package pageobjects.admin;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;
import static org.junit.Assert.*;

/**
 * Author: Ruarcc McAloon
 * Date: 13/02/14
 * Time: 08:55
 */
public class AdminPage extends LoadableComponent<AdminPage> {

    @FindBy(xpath="//a[contains(text(),'Projects')]")
    @CacheLookup
    private WebElement projects;

    private WebDriver driver;
    private String url = "http://rsr.uat.akvo.org/admin/";
    private String title = "Site administration | Akvo RSR site admin";

    public AdminPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    @Override
    protected void load() {
        this.driver.get(url);
    }

    @Override
    protected void isLoaded()  {
        assertTrue(driver.getTitle().equals(title));
    }

    public void goToProjectPage() {
        projects.click();
    }
}
