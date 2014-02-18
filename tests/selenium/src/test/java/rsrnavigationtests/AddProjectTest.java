package rsrnavigationtests;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;
import pageobjects.admin.AdminPage;
import pageobjects.admin.AllProjectsPage;
import pageobjects.admin.LoginPage;
import utils.TestData;

import java.io.IOException;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

/**
 * Author: Ruarcc McAloon
 * Date: 10/02/14
 * Time: 13:20
 */
public class AddProjectTest {

    private WebDriver driver;
    private TestData testData;
    private List<String[]> projectDetails;

    @Before
    public void setUp(){
        driver = new FirefoxDriver();
        testData = new TestData("src/test/resources/TestData.csv");
        try{
            projectDetails = testData.getTestDataFromSource();
        } catch (IOException e){
           // fail("issue") ;
        }
    }

    @Test
    public void createAndPublishNewProjectTest(){
        LoginPage loginPage = new LoginPage(driver);
        loginPage.logInTestAdmin();

        AdminPage adminPage = new AdminPage(driver);
        adminPage.goToProjectPage();

        AllProjectsPage projectsPage = new AllProjectsPage(driver);
        projectsPage.goToAddProjectPage();

        driver.findElement(By.name("title")).sendKeys("Selenium Test Project");
        driver.findElement(By.name("subtitle")).sendKeys("test");
        driver.findElement(By.name("project_plan_summary")).sendKeys("test");
        driver.findElement(By.name("background")).sendKeys("test");
        driver.findElement(By.name("current_status")).sendKeys("test");
        driver.findElement(By.name("sustainability")).sendKeys("test");
        driver.findElement(By.name("goals_overview")).sendKeys("test");

        Select partnerSelect = new Select(driver.findElement(By.id("id_partnerships-0-partner_type")));
        partnerSelect.selectByVisibleText("Field partner");

        Select categorySelect = new Select(driver.findElement(By.id("id_categories")));
        categorySelect.selectByVisibleText("Agriculture (Economic development)");

        driver.findElement(By.name("_save")).click();

        driver.findElement(By.xpath("//a[contains(text(),'Home')]")).click();
        driver.findElement(By.xpath("//a[contains(text(),'Publishing statuses')]")).click();
        driver.findElement(By.xpath("//a[contains(text(), 'Selenium Test Project')]")).click();

        Select statusSelect = new Select(driver.findElement(By.id("id_status")));
        statusSelect.selectByVisibleText("Published");

        driver.findElement(By.name("_save")).click();

        driver.get("http://rsrnavigationtests.uat.akvo.org/projects/all/");

        assertTrue(driver.getPageSource().contains("Selenium Test Project"));
    }

    @After
    public void tearDown(){
        driver.close();
    }
}
