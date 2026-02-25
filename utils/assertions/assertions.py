class Assertions:

    def assert_text(self, actual_text, expected_text):
        assert actual_text == expected_text, (f"Текст не соответствует ожидаемому."
                                              f"Ожидали {expected_text}, получили {actual_text}")


    def assert_url(self, actual_url, expected_url):
        assert actual_url == expected_url, (f"Не удалось попасть на страницу."
                                              f"Ожидали {expected_url}, получили {actual_url}")

    def assert_true(self, condition: bool, message: str):
        assert condition, message

    def assert_page_texts(self, actual_texts, expected_texts):
        mismatches = []
        for key, expected in expected_texts.items():
            actual = actual_texts.get(key)
            if actual != expected:
                mismatches.append(f"  {key}: ожидали '{expected}', получили '{actual}'")
        assert not mismatches, (
            f"Тексты страницы не соответствуют ожидаемым:\n" + "\n".join(mismatches)
        )
