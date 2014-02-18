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
 * Time: 08:40
 */
public class LoginPage extends LoadableComponent<LoginPage> {

    private WebElement username;
    private WebElement password;
    @FindBy(xpath="//input[@value='Log in']")
    @CacheLookup
    private WebElement loginButton;

    private WebDriver driver;
    private String url = "http://rsr.uat.akvo.org/admin/";
    private String title = "Site administration | Akvo RSR site admin";

    public LoginPage(WebDriver driver) {
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

    public void logInTestAdmin() {
        username.sendKeys("AutomatedTestUser");
        password.sendKeys("testpassword");
        loginButton.click();
    }
}

