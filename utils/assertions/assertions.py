class Assertions:

    def assert_text(self, actual_text, expected_text):
        assert actual_text == expected_text, (f"Текст не соответствует ожидаемому."
                                              f"Ожидали {expected_text}, получили {actual_text}")


    def assert_url(self, actual_url, expected_url):
        assert actual_url == expected_url, (f"Не удалось попасть на страницу."
                                              f"Ожидали {expected_url}, получили {actual_url}")