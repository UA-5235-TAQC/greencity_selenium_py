[1mdiff --git a/components/create_edit_news/image_component.py b/components/create_edit_news/image_component.py[m
[1mindex 9b326dc..2f91c1d 100644[m
[1m--- a/components/create_edit_news/image_component.py[m
[1m+++ b/components/create_edit_news/image_component.py[m
[36m@@ -51,7 +51,8 @@[m [mclass ImageComponent(BaseComponent):[m
     @allure.step("Upload image from file absolute path: {file_absolute_path}")[m
     def upload_image(self, file_absolute_path: str):[m
         """Uploads an image file by sending the file path to the hidden file input."""[m
[31m-        self.upload_input.send_keys(file_absolute_path)[m
[32m+[m[32m        input_element = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")[m
[32m+[m[32m        input_element.send_keys(file_absolute_path)[m
         return self[m
 [m
     @allure.step("Get image input field value")[m
[36m@@ -77,7 +78,10 @@[m [mclass ImageComponent(BaseComponent):[m
     @allure.step("Get source URL of the uploaded image")[m
     def get_uploaded_image_src(self) -> str:[m
         """Returns the 'src' attribute of the uploaded image element."""[m
[31m-        return self.uploaded_image.get_attribute("src")[m
[32m+[m[32m        try:[m
[32m+[m[32m            return self._has_image_src_prefix(self.uploaded_image, "blob:")[m
[32m+[m[32m        except (ElementNotFoundException, Exception):[m
[32m+[m[32m            return False[m
 [m
     @allure.step("Get source URL of the preview image")[m
     def get_preview_image_src(self) -> str:[m
[36m@@ -97,7 +101,10 @@[m [mclass ImageComponent(BaseComponent):[m
     @allure.step("Check if uploaded image (blob:) is displayed")[m
     def is_uploaded_image_present(self) -> bool:[m
         """Checks if the displayed image is a blob URL (indicating a successful local upload)."""[m
[31m-        return self._has_image_src_prefix(self.uploaded_image, "blob:")[m
[32m+[m[32m        try:[m
[32m+[m[32m            return self._has_image_src_prefix(self.uploaded_image, "blob:")[m
[32m+[m[32m        except (ElementNotFoundException, Exception):[m
[32m+[m[32m            return False[m
 [m
     @allure.step("Click Submit crop")[m
     def submit_crop(self):[m
[1mdiff --git a/tests/ui/test_basic_preview_functionality.py b/tests/ui/test_basic_preview_functionality.py[m
[1mindex 3801f52..4b68440 100644[m
[1m--- a/tests/ui/test_basic_preview_functionality.py[m
[1m+++ b/tests/ui/test_basic_preview_functionality.py[m
[36m@@ -22,7 +22,7 @@[m [mclass TestNewsDetails:[m
         4. Verify navigation back to the creation page.[m
     """)[m
     @allure.testcase("https://github.com/UA-5235-TAQC/greencity_selenium5235/issues/10")[m
[31m-    @allure.severity(allure.severity_level.CRITICAL)[m
[32m+[m[32m    @allure.severity(allure.severity_level.MINOR)[m
     def test_news_preview_check(self, get_driver):[m
         create_news_page = CreateNewsPage(get_driver)[m
         news_page = NewsPage(get_driver)[m
