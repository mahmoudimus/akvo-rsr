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
public class AllProjectsPage extends LoadableComponent<AllProjectsPage> {

    @FindBy(xpath="//a[contains(text(),'Add project')]")
    @CacheLookup
    private WebElement addProject;

    private WebDriver driver;
    private String url = "http://rsr.uat.akvo.org/admin/rsr/project";
    private String title = "Select project to change | Akvo RSR site admin";

    public AllProjectsPage(WebDriver driver) {
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

    public void goToAddProjectPage() {
        addProject.click();
    }
}