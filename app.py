import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Trà Sữa Thanh Hân",
    page_icon="🧋",
    layout="wide"
)

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa socola": 32000,
    "Trà sữa matcha": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 32000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
    "XL": 10000,
}

# =========================
# KHỞI TẠO SESSION
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

# =========================
# HÀM TÍNH TIỀN
# =========================
def calculate_item_price(drink, size, topping):
    return (
        MENU[drink]
        + SIZE_PRICE[size]
        + TOPPINGS[topping]
    )


def format_money(amount):
    return f"{amount:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUẢN LÝ HÓA ĐƠN QUÁN TRÀ SỮA")
st.caption("Ứng dụng tính tiền và xuất hóa đơn bằng Streamlit")

st.divider()

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

# =========================
# CHỌN MÓN
# =========================
st.subheader("🧋 Thêm món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / thức uống",
        list(MENU.keys())
    )

    size = st.selectbox(
        "Size",
        ["M", "L", "XL"]
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

with col2:
    topping = st.selectbox(
        "Loại topping",
        list(TOPPINGS.keys())
    )

    sugar = st.select_slider(
        "Mức độ đường",
        options=[
            "0%",
            "30%",
            "50%",
            "70%",
            "100%"
        ],
        value="70%"
    )

    ice = st.select_slider(
        "Mức độ đá",
        options=[
            "Không đá",
            "30%",
            "50%",
            "70%",
            "100%"
        ],
        value="70%"
    )

# =========================
# HIỂN THỊ GIÁ MÓN
# =========================
unit_price = calculate_item_price(
    drink,
    size,
    topping
)

total_item = unit_price * quantity

st.info(
    f"💰 Đơn giá: **{format_money(unit_price)}**  |  "
    f"Thành tiền: **{format_money(total_item)}**"
)

# =========================
# NÚT THÊM MÓN
# =========================
if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    use_container_width=True
):

    if not customer_name.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước.")
    else:
        item = {
            "Tên món": drink,
            "Size": size,
            "Topping": topping,
            "Đường": sugar,
            "Đá": ice,
            "Số lượng": quantity,
            "Đơn giá": unit_price,
            "Thành tiền": total_item
        }

        st.session_state.cart.append(item)

        st.success(
            f"✅ Đã thêm {quantity} x {drink} vào hóa đơn!"
        )

# =========================
# GIỎ HÀNG / DANH SÁCH MÓN
# =========================
st.divider()
st.subheader("🛒 Danh sách món trong hóa đơn")

if len(st.session_state.cart) == 0:

    st.info("Chưa có món nào trong hóa đơn.")

else:

    # Hiển thị bảng
    display_data = []

    for i, item in enumerate(st.session_state.cart, start=1):
        display_data.append({
            "STT": i,
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "SL": item["Số lượng"],
            "Đơn giá": format_money(item["Đơn giá"]),
            "Thành tiền": format_money(item["Thành tiền"])
        })

    df_display = pd.DataFrame(display_data)

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

    # Tổng tiền
    subtotal = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    st.markdown(
        f"""
        <div style="
            background-color:#f0f2f6;
            padding:20px;
            border-radius:10px;
            text-align:right;
        ">
            <h3>Tổng tiền: {format_money(subtotal)}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # =========================
    # XÓA MÓN
    # =========================
    st.subheader("🗑️ Quản lý món")

    delete_index = st.selectbox(
        "Chọn món muốn xóa",
        range(len(st.session_state.cart)),
        format_func=lambda i:
            f"{i + 1}. {st.session_state.cart[i]['Tên món']} "
            f"- {st.session_state.cart[i]['Size']}"
    )

    col_delete1, col_delete2 = st.columns(2)

    with col_delete1:
        if st.button(
            "🗑️ Xóa món đang chọn",
            use_container_width=True
        ):
            st.session_state.cart.pop(delete_index)
            st.rerun()

    with col_delete2:
        if st.button(
            "❌ Xóa toàn bộ hóa đơn",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.session_state.invoice = None
            st.rerun()

    # =========================
    # THANH TOÁN
    # =========================
    st.divider()

    st.subheader("💳 Thanh toán")

    payment_method = st.selectbox(
        "Phương thức thanh toán",
        [
            "Tiền mặt",
            "Chuyển khoản",
            "Ví điện tử"
        ]
    )

    if st.button(
        "💰 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():
            st.warning("⚠️ Vui lòng nhập tên khách hàng.")

        else:

            now = datetime.now()

            invoice_number = (
                "HD"
                + now.strftime("%Y%m%d")
                + now.strftime("%H%M%S")
            )

            invoice = {
                "Mã hóa đơn": invoice_number,
                "Khách hàng": customer_name,
                "Thời gian": now.strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                "Phương thức thanh toán": payment_method,
                "Danh sách món": st.session_state.cart.copy(),
                "Tổng tiền": subtotal
            }

            st.session_state.invoice = invoice

            st.success(
                "🎉 Thanh toán thành công!"
            )

# =========================
# HÓA ĐƠN
# =========================
if st.session_state.invoice is not None:

    st.divider()

    st.subheader("🧾 HÓA ĐƠN THANH TOÁN")

    invoice = st.session_state.invoice

    st.markdown(
        f"""
        <div style="
            border:1px solid #cccccc;
            padding:25px;
            border-radius:12px;
            background-color:white;
        ">

        <h2 style="text-align:center;">
        🧋 TRÀ SỮA THANH HÂN
        </h2>

        <p style="text-align:center;">
        HÓA ĐƠN THANH TOÁN
        </p>

        <hr>

        <p><b>Mã hóa đơn:</b> {invoice["Mã hóa đơn"]}</p>

        <p><b>Khách hàng:</b> {invoice["Khách hàng"]}</p>

        <p><b>Thời gian:</b> {invoice["Thời gian"]}</p>

        <p>
        <b>Thanh toán:</b>
        {invoice["Phương thức thanh toán"]}
        </p>

        <hr>
        """,
        unsafe_allow_html=True
    )

    # Danh sách món trong hóa đơn
    invoice_rows = []

    for i, item in enumerate(
        invoice["Danh sách món"],
        start=1
    ):

        invoice_rows.append({
            "STT": i,
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "SL": item["Số lượng"],
            "Đơn giá": format_money(item["Đơn giá"]),
            "Thành tiền": format_money(item["Thành tiền"])
        })

    invoice_df = pd.DataFrame(invoice_rows)

    st.dataframe(
        invoice_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"""
        <hr>

        <h2 style="text-align:right;">
        TỔNG CỘNG: {format_money(invoice["Tổng tiền"])}
        </h2>

        <p style="text-align:center;">
        Cảm ơn quý khách và hẹn gặp lại! ❤️
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # XUẤT HÓA ĐƠN EXCEL
    # =========================
    st.subheader("📥 Xuất hóa đơn")

    export_data = []

    for item in invoice["Danh sách món"]:

        export_data.append({
            "Mã hóa đơn": invoice["Mã hóa đơn"],
            "Khách hàng": invoice["Khách hàng"],
            "Thời gian": invoice["Thời gian"],
            "Phương thức thanh toán":
                invoice["Phương thức thanh toán"],
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "Số lượng": item["Số lượng"],
            "Đơn giá": item["Đơn giá"],
            "Thành tiền": item["Thành tiền"]
        })

    export_df = pd.DataFrame(export_data)

    # Tạo file Excel trong bộ nhớ
    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Hoa Don"
        )

    excel_buffer.seek(0)

    st.download_button(
        label="📊 Xuất hóa đơn Excel",
        data=excel_buffer,
        file_name=f"{invoice['Mã hóa đơn']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # =========================
    # XUẤT HÓA ĐƠN CSV
    # =========================
    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📄 Xuất hóa đơn CSV",
        data=csv_data,
        file_name=f"{invoice['Mã hóa đơn']}.csv",
        mime="text/csv",
        use_container_width=True
    )
