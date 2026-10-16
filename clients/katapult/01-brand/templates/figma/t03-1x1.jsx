const imgHandIphone = "assets/505204f5-cb52-452e-8b16-b46efbb3f558.png";
const imgVector12 = "assets/a035e41c-8fb0-45d2-a2c3-37ce607955c0.svg";
const imgLayer1 = "assets/a6eb240d-e992-48b2-aba0-141f9cc94aad.svg";

export default function Template03SplitPhoneHand() {
  return (
    <div className="relative size-full" data-node-id="547:1072" data-name="template-03-split-phone-hand">
      <div className="-translate-y-1/2 absolute bg-[#ed5370] h-[1200px] left-0 top-1/2 w-[550px]" data-node-id="547:1073" data-name="photo-right" />
      <div className="absolute h-[1200px] right-0 top-0 w-[650px]" data-node-id="547:1074">
        <div className="-translate-y-1/2 absolute bg-[#131540] h-[1200px] left-0 top-1/2 w-[650px]" data-node-id="547:1075" data-name="photo-right" />
        <div className="absolute h-[1262.636px] left-[-110px] mix-blend-soft-light top-[284px] w-[2429.41px]" data-node-id="547:1076">
          <div className="absolute inset-[-9.64%_-1.42%_-9.64%_0]">
            <img alt="" className="block max-w-none size-full" src={imgVector12} />
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[1042px] items-center justify-between left-[57px] top-[94px] w-[536px]" data-node-id="547:1077">
          <div className="content-stretch flex flex-col gap-[48px] items-center relative shrink-0 w-full" data-node-id="547:1078" data-name="copy">
            <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1079" data-name="Layer_1">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
            </div>
            <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0] not-italic relative shrink-0 text-[82.324px] text-center text-white tracking-[-3.293px] w-[536px]" data-node-id="547:1085">
              <p className="leading-none mb-0">Open the app</p>
              <p className="leading-none mb-0">Find it fast</p>
              <p className="leading-none">Make it yours.</p>
            </div>
            <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] text-center w-[424px]" data-node-id="547:1086">
              Browse, apply, and start shopping right from your phone.
            </p>
            <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1087" data-name="Button">
              <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1087;2485:67">
                Leap Forward
              </p>
            </div>
          </div>
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[#d8d8d8] text-[15px] text-center w-[326px]" data-node-id="547:1088">
            Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
          </p>
        </div>
      </div>
      <div className="absolute h-[1398px] left-[-184px] top-[148px] w-[847px]" data-node-id="547:1089" data-name="hand-iphone">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[133.91%] left-0 max-w-none top-[-33.91%] w-[147.38%]" src={imgHandIphone} />
        </div>
      </div>
    </div>
  );
}