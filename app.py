import streamlit as st

from converter import (
    extract_text_from_pdf,
    create_word,
    create_csv,
    is_scanned_pdf
)


st.set_page_config(
    page_title="Professional PDF Converter",
    layout="centered"
)


st.title(
    "PDF to Editable Word & CSV Converter"
)

st.write(
    """
    Upload a PDF file.

    The application automatically detects whether
    the PDF is a normal PDF or a scanned PDF.
    """
)


uploaded_file = st.file_uploader(
    "Choose PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    pdf_bytes = uploaded_file.getvalue()

    scanned = is_scanned_pdf(
        pdf_bytes
    )

    if scanned:

        st.warning(
            "Scanned PDF detected. OCR will be used."
        )

    else:

        st.info(
            "Digital PDF detected. Layout conversion will be used."
        )

    if st.button(
        "Convert PDF",
        type="primary"
    ):

        try:

            with st.spinner(
                "Converting PDF... This may take some time."
            ):

                # Extract text
                pages = extract_text_from_pdf(
                    pdf_bytes
                )

                # Word
                word_file = create_word(
                    pdf_bytes
                )

                # CSV
                csv_file = create_csv(
                    pages
                )

            st.success(
                "Conversion completed successfully!"
            )

            st.divider()

            st.subheader(
                "Download Files"
            )

            # Original filename
            original_name = (
                uploaded_file.name
                .rsplit(".", 1)[0]
            )

            st.download_button(
                label="Download Editable Word",
                data=word_file,
                file_name=f"{original_name}.docx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                )
            )

            st.download_button(
                label="Download CSV",
                data=csv_file,
                file_name=f"{original_name}.csv",
                mime="text/csv"
            )

            st.divider()

            st.subheader(
                "Extracted Text Preview"
            )

            for page in pages:

                with st.expander(
                    f"Page {page['page']}"
                ):

                    st.text(
                        page["text"]
                    )

        except Exception as error:

            st.error(
                f"Conversion failed: {error}"
            )